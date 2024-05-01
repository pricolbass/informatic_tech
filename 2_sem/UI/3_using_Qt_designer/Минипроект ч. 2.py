from PyQt6.QtWidgets import QApplication, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QLineEdit, QMainWindow, \
    QWidget, QGridLayout
from PyQt6.QtGui import QFont
from PyQt6 import uic
import shelve


class DecisionHelperApp(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('design.ui', self)
        self.argument_widgets = {}
        self.initUI()
        self.loadData()

    def initUI(self):
        self.setWindowTitle('Помощник в принятии решений')
        self.centralwidget = self.findChild(QWidget, 'centralwidget')

        self.main_layout = self.findChild(QVBoxLayout, 'main_layout')

        self.question_layout = self.findChild(QHBoxLayout, 'add_question')
        self.question_input = self.findChild(QLineEdit, 'question_input')
        self.set_question_button = self.findChild(QPushButton, 'set_question_button')
        self.question_label = self.findChild(QLabel, 'question')

        self.argument_layout = self.findChild(QHBoxLayout, 'add_args')
        self.argument_input = self.findChild(QLineEdit, 'arg_input')
        self.add_argument_button = self.findChild(QPushButton, 'set_arg_button')

        self.reset_button = self.findChild(QPushButton, 'reset_button')

        self.count_labels_layout = self.findChild(QGridLayout, 'labels_count')
        self.main_layout.addLayout(self.count_labels_layout)

        self.set_question_button.clicked.connect(self.setQuestion)
        self.add_argument_button.clicked.connect(self.addArgument)
        self.reset_button.clicked.connect(self.resetCounts)

    def loadData(self):
        with shelve.open('decision_helper_data') as data:
            self.arguments = data.get('arguments', {})
            self.question = data.get('question', '')
            self.question_set = data.get('question_set', False)

        if self.question_set:
            self.question_input.hide()
            self.set_question_button.hide()
            self.question_label.setText(f"Вопрос: {self.question}")

        for argument_name, count in self.arguments.items():
            self.createCountLabel(argument_name, count)

        if not self.arguments:
            self.add_argument_button.show()
            self.argument_input.show()
        else:
            self.add_argument_button.hide()
            self.argument_input.hide()

        self.updateDisplay()

    def saveData(self):
        with shelve.open('decision_helper_data') as data:
            data['arguments'] = self.arguments
            data['question'] = self.question
            data['question_set'] = self.question_set

    def addArgument(self):
        argument_name = self.argument_input.text()
        if argument_name and argument_name not in self.arguments:
            self.arguments[argument_name] = 0
            self.argument_input.clear()
            self.createCountLabel(argument_name)
            self.saveData()

    def createCountLabel(self, argument_name, count=0):
        label = QLabel(f"{argument_name}: {count}", self)
        font = QFont()
        font.setPointSize(12)
        label.setFont(font)
        self.count_labels_layout.addWidget(label)
        button = QPushButton(argument_name, self)
        button.setMinimumSize(747, 50)
        button.clicked.connect(lambda: self.incrementCount(argument_name, label))
        self.main_layout.insertWidget(self.main_layout.count() - 1 - self.count_labels_layout.count(), button)
        self.arguments[argument_name] = count
        self.argument_widgets[argument_name] = (button, label)

    def incrementCount(self, argument_name, label):
        self.arguments[argument_name] += 1
        label.setText(f"{argument_name}: {self.arguments[argument_name]}")
        self.saveData()

    def resetCounts(self):
        self.arguments = {}
        self.question = ''
        self.question_set = False
        self.question_input.clear()
        self.argument_input.clear()
        self.add_argument_button.show()
        self.argument_input.show()

        for button, label in self.argument_widgets.values():
            button.deleteLater()
            label.deleteLater()
        self.argument_widgets.clear()

        self.saveData()
        self.updateDisplay()

    def clearCountLabels(self):
        while self.count_labels_layout.count():
            item = self.count_labels_layout.takeAt(0)
            widget = item.widget()
            if widget is not None:
                widget.deleteLater()

    def setQuestion(self):
        self.question = self.question_input.text()
        self.question_set = True
        self.saveData()
        self.updateDisplay()

    def updateDisplay(self):
        self.question_label.setText(f"Вопрос: {self.question}")
        if self.question_set:
            self.question_input.hide()
            self.set_question_button.hide()
        else:
            self.question_input.show()
            self.set_question_button.show()


if __name__ == '__main__':
    app = QApplication([])
    window = DecisionHelperApp()
    window.show()
    app.exec()
