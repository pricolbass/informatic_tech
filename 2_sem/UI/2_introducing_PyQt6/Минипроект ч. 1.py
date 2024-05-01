from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QLabel, QLineEdit
import shelve


class DecisionHelperApp(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.loadData()

    def initUI(self):
        self.setWindowTitle('Помощник в принятии решений')
        self.layout = QVBoxLayout(self)

        self.question_input = QLineEdit(self)
        self.set_question_button = QPushButton('Установить вопрос', self)
        self.for_button = QPushButton('За', self)
        self.against_button = QPushButton('Против', self)
        self.reset_button = QPushButton('Сброс', self)
        self.question_label = QLabel('Вопрос: ', self)
        self.for_label = QLabel('За: 0', self)
        self.against_label = QLabel('Против: 0', self)

        self.layout.addWidget(self.question_input)
        self.layout.addWidget(self.set_question_button)
        self.layout.addWidget(self.question_label)
        self.layout.addWidget(self.for_button)
        self.layout.addWidget(self.against_button)
        self.layout.addWidget(self.reset_button)
        self.layout.addWidget(self.for_label)
        self.layout.addWidget(self.against_label)

        self.for_button.clicked.connect(lambda: self.incrementCount('for'))
        self.against_button.clicked.connect(lambda: self.incrementCount('against'))
        self.reset_button.clicked.connect(self.resetCounts)
        self.set_question_button.clicked.connect(self.setQuestion)

    def loadData(self):
        with shelve.open('decision_helper_data') as data:
            self.counts = data.get('counts', {'for': 0, 'against': 0})
            self.question = data.get('question', '')
            self.question_set = data.get('question_set', False)
        self.updateDisplay()

    def saveData(self):
        with shelve.open('decision_helper_data') as data:
            data['counts'] = self.counts
            data['question'] = self.question
            data['question_set'] = self.question_set

    def incrementCount(self, key):
        self.counts[key] += 1
        self.saveData()
        self.updateDisplay()

    def resetCounts(self):
        self.counts = {'for': 0, 'against': 0}
        self.question = ''
        self.question_set = False
        self.question_input.clear()
        self.question_input.show()
        self.set_question_button.show()
        self.saveData()
        self.updateDisplay()

    def setQuestion(self):
        self.question = self.question_input.text()
        self.question_set = True
        self.question_input.hide()
        self.set_question_button.hide()
        self.saveData()
        self.updateDisplay()

    def updateDisplay(self):
        self.question_label.setText(f"Вопрос: {self.question}")
        self.for_label.setText(f"За: {self.counts['for']}")
        self.against_label.setText(f"Против: {self.counts['against']}")

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
