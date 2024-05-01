import sys
from PyQt6.QtWidgets import (QApplication, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QLineEdit,
                             QListWidget, QLCDNumber, QComboBox, QMessageBox)
from PyQt6.QtCore import QEvent
import json


class DragDropListWidget(QListWidget):
    def __init__(self, listType, parent=None):
        super().__init__(parent)
        self.listType = listType
        self.setDragDropMode(QListWidget.DragDropMode.InternalMove)
        self.setSelectionMode(QListWidget.SelectionMode.SingleSelection)
        self.setDragEnabled(True)
        self.viewport().setAcceptDrops(True)
        self.setDropIndicatorShown(True)
        self.installEventFilter(self)

    def eventFilter(self, source, event):
        if event.type() == QEvent.Type.ChildRemoved:
            self.parent().updateArgumentsOrder(self.listType)
            return True
        return super().eventFilter(source, event)

    def mouseDoubleClickEvent(self, event):
        item = self.currentItem()
        if item:
            reply = QMessageBox.question(self, 'Удаление аргумента',
                                         f"Вы точно хотите удалить аргумент \"{item.text()}\"?",
                                         QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
                                         QMessageBox.StandardButton.No)
            if reply == QMessageBox.StandardButton.Yes:
                currentIndex = self.currentRow()
                self.takeItem(currentIndex)
                self.parent().deleteArgument(self.listType, item.text())


class DecisionHelper(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Помощник в принятии решений")
        self.questions = {}
        self.currentQuestion = ""
        self.initUI()
        self.loadData()

    def initUI(self):
        self.layout = QVBoxLayout(self)

        self.questionInput = QLineEdit()
        self.questionInput.setPlaceholderText("Введите вопрос...")
        self.layout.addWidget(self.questionInput)

        self.addQuestionButton = QPushButton('Добавить вопрос')
        self.addQuestionButton.clicked.connect(self.addQuestion)
        self.layout.addWidget(self.addQuestionButton)

        self.questionDisplay = QLabel("Текущий вопрос: Нет")
        self.layout.addWidget(self.questionDisplay)

        self.questionSelector = QComboBox()
        self.questionSelector.currentIndexChanged.connect(self.changeQuestion)
        self.layout.addWidget(self.questionSelector)

        self.argumentInput = QLineEdit()
        self.argumentInput.setPlaceholderText("Введите аргумент...")
        self.layout.addWidget(self.argumentInput)

        argumentsLayout = QHBoxLayout()

        proLayout = QVBoxLayout()
        self.addProArgumentButton = QPushButton('Добавить аргумент "За"')
        self.addProArgumentButton.clicked.connect(lambda: self.addArgument("pro"))
        proLayout.addWidget(self.addProArgumentButton)
        self.proArgumentsList = DragDropListWidget("pro", self)
        proLayout.addWidget(self.proArgumentsList)
        self.proLCDNumber = QLCDNumber()
        proLayout.addWidget(self.proLCDNumber)

        conLayout = QVBoxLayout()
        self.addConArgumentButton = QPushButton('Добавить аргумент "Против"')
        self.addConArgumentButton.clicked.connect(lambda: self.addArgument("con"))
        conLayout.addWidget(self.addConArgumentButton)
        self.conArgumentsList = DragDropListWidget("con", self)
        conLayout.addWidget(self.conArgumentsList)
        self.conLCDNumber = QLCDNumber()
        conLayout.addWidget(self.conLCDNumber)

        argumentsLayout.addLayout(proLayout)
        argumentsLayout.addLayout(conLayout)

        self.layout.addLayout(argumentsLayout)

        self.resetButton = QPushButton('Сброс')
        self.resetButton.clicked.connect(self.resetCounts)
        self.layout.addWidget(self.resetButton)

    def loadData(self):
        try:
            with open("data.json", "r") as f:
                self.questions = json.load(f)
            self.questionSelector.addItems(self.questions.keys())
            self.changeQuestion()
        except FileNotFoundError:
            self.questions = {}

    def saveData(self):
        with open("data.json", "w") as f:
            json.dump(self.questions, f)

    def addQuestion(self):
        question = self.questionInput.text()
        if question and question not in self.questions:
            self.questions[question] = {"pro": [], "con": []}
            self.questionSelector.addItem(question)
            self.questionSelector.setCurrentText(question)
            self.questionInput.clear()
            self.saveData()

    def changeQuestion(self):
        self.currentQuestion = self.questionSelector.currentText()
        self.questionDisplay.setText(f"Текущий вопрос: {self.currentQuestion}")
        self.updateArgumentsDisplay()

    def addArgument(self, listType):
        argument = self.argumentInput.text()
        if argument:
            self.questions[self.currentQuestion][listType].append(argument)
            self.argumentInput.clear()
            self.updateArgumentsDisplay()
            self.saveData()

    def deleteArgument(self, listType, argumentText):
        self.questions[self.currentQuestion][listType] = [arg for arg in self.questions[self.currentQuestion][listType]
                                                          if arg != argumentText]
        self.updateArgumentsDisplay()
        self.saveData()

    def updateArgumentsDisplay(self):
        self.proArgumentsList.clear()
        self.conArgumentsList.clear()
        if self.currentQuestion:
            for arg in self.questions[self.currentQuestion]["pro"]:
                self.proArgumentsList.addItem(arg)
            for arg in self.questions[self.currentQuestion]["con"]:
                self.conArgumentsList.addItem(arg)
        self.updateLCDNumbers()

    def updateLCDNumbers(self):
        if self.currentQuestion:
            self.proLCDNumber.display(len(self.questions[self.currentQuestion]["pro"]))
            self.conLCDNumber.display(len(self.questions[self.currentQuestion]["con"]))

    def resetCounts(self):
        if self.currentQuestion:
            self.questions[self.currentQuestion] = {"pro": [], "con": []}
            self.updateArgumentsDisplay()
            self.saveData()

    def updateArgumentsOrder(self, listType):
        newOrder = [self.proArgumentsList.item(i).text() for i in
                    range(self.proArgumentsList.count())] if listType == "pro" else [
            self.conArgumentsList.item(i).text() for i in range(self.conArgumentsList.count())]
        self.questions[self.currentQuestion][listType] = newOrder
        self.saveData()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = DecisionHelper()
    ex.show()
    sys.exit(app.exec())
