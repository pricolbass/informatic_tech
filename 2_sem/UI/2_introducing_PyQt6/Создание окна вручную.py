from PyQt6 import QtWidgets, QtCore
import sys
import random


class MyWindow(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Программа на PyQt")
        self.resize(400, 100)

        self.clickCount = 0
        self.currentColor = '#FFFFFF'
        self.btnPos = QtCore.QPoint(0, 30)
        self.initUI()

    def initUI(self):
        self.label = QtWidgets.QLabel("Привет, мир!", self)
        self.label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)

        self.labelClick = QtWidgets.QLabel("", self)
        self.labelClick.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)

        self.btn = QtWidgets.QPushButton("&Закрыть окно", self)
        self.btn.clicked.connect(self.move_btn)

        self.btnCount = QtWidgets.QPushButton("Нажатий: 0", self)
        self.btnCount.clicked.connect(self.increase_count)
        self.clickCount = 0

        self.btnYes = QtWidgets.QPushButton("ДА", self)
        self.btnNo = QtWidgets.QPushButton("НЕТ", self)
        self.btnYes.clicked.connect(self.buttonClicked)
        self.btnNo.clicked.connect(self.buttonClicked)

        self.btnColor = QtWidgets.QPushButton("Сменить цвет", self)
        self.btnColor.clicked.connect(self.changeColor)

        # Расположение кнопок по горизонтали
        hLayout = QtWidgets.QHBoxLayout()
        hLayout.addStretch()
        hLayout.addWidget(self.btn)
        hLayout.addWidget(self.btnCount)
        hLayout.addWidget(self.btnYes)
        hLayout.addWidget(self.btnNo)
        hLayout.addWidget(self.btnColor)
        hLayout.addStretch()

        vLayout = QtWidgets.QVBoxLayout()
        vLayout.addWidget(self.label)
        vLayout.addWidget(self.labelClick)
        vLayout.addLayout(hLayout)

        self.setLayout(vLayout)
        self.show()

        self.updateUI()

    def move_btn(self):
        self.btnPos += QtCore.QPoint(10, 0)
        if self.btnPos.x() + self.btn.width() > self.width():
            self.btnPos.setX(10)
        self.labelClick.setText("")
        self.btn.move(self.btnPos)

    def increase_count(self):
        sender = self.sender()
        self.clickCount += 1
        self.labelClick.setText(f"Нажата кнопка: {sender.text()}")
        self.btnCount.setText(f"Нажатий: {self.clickCount}")
        self.updateUI()

    def buttonClicked(self):
        sender = self.sender()
        self.labelClick.setText(f"Нажата кнопка: {sender.text()}")
        self.updateUI()

    def changeColor(self):
        sender = self.sender()
        self.labelClick.setText(f"Нажата кнопка: {sender.text()}")
        self.currentColor = f'#{random.randint(0, 0xFFFFFF):06x}'
        self.updateUI()

    def updateUI(self):
        self.setStyleSheet(f"background-color: {self.currentColor};")
        self.btnCount.setText(f"Нажатий: {self.clickCount}")
        self.btn.move(self.btnPos)


app = QtWidgets.QApplication(sys.argv)
window = MyWindow()
sys.exit(app.exec())
