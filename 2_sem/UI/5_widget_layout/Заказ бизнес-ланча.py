from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QGroupBox, QRadioButton, QCheckBox, \
    QPushButton, QMessageBox, QLabel, QFrame
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont
import sys
import json
from os.path import exists


class LunchOrderApp(QWidget):
    def __init__(self):
        super().__init__()
        self.orders = self.loadOrders()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Заказ Бизнес-Ланча')
        self.setGeometry(100, 100, 800, 600)
        mainLayout = QHBoxLayout()

        orderFormLayout = QVBoxLayout()

        self.createCategory(orderFormLayout, "Эликсиры", ["Эликсир Мощи", "Эликсир Скорости", "Эликсир Стойкости"])
        self.createCategory(orderFormLayout, "Основные блюда",
                            ["Сваренный Дикий Рис", "Пирог с Тыквой", "Лесной Жаркое"])
        self.createCategory(orderFormLayout, "Десерты", ["Медовый Пирог", "Пирожное с Ягодами", "Фруктовое Желе"])
        self.createCategory(orderFormLayout, "Зелья", ["Зелье Жизненной Силы", "Зелье Восстановления Стамины"])
        self.createCategory(orderFormLayout, "Закуски", ["Жареные Грибы", "Копченая Рыба", "Овощное Рагу"])

        self.orderButton = QPushButton('Заказать')
        self.orderButton.clicked.connect(self.placeOrder)
        orderFormLayout.addWidget(self.orderButton)

        self.orderButton.setEnabled(False)

        self.resetOrdersButton = QPushButton('Сбросить заказы')
        self.resetOrdersButton.clicked.connect(self.resetOrders)
        orderFormLayout.addWidget(self.resetOrdersButton)

        self.ordersLayout = QVBoxLayout()
        self.updateOrdersDisplay()

        mainLayout.addLayout(orderFormLayout)
        mainLayout.addLayout(self.ordersLayout)

        self.setLayout(mainLayout)

    def createCategory(self, layout, name, options):
        groupBox = QGroupBox(name)
        vbox = QVBoxLayout()

        checkBox = QCheckBox("Выбрать")
        checkBox.stateChanged.connect(self.updateOrderButtonState)
        vbox.addWidget(checkBox)

        radioButtons = []
        for option in options:
            radioButton = QRadioButton(option)
            radioButton.setEnabled(False)
            checkBox.stateChanged.connect(lambda state, button=radioButton: button.setEnabled(state == 2))
            vbox.addWidget(radioButton)
            radioButtons.append(radioButton)
        groupBox.radioButtons = radioButtons

        groupBox.setLayout(vbox)
        layout.addWidget(groupBox)

    def updateOrderButtonState(self):
        checkBoxes = self.findChildren(QCheckBox)
        selectedCount = sum(1 for box in checkBoxes if box.isChecked())
        self.orderButton.setEnabled(selectedCount >= 2)

    def placeOrder(self):
        order = {}
        for groupBox in self.findChildren(QGroupBox):
            category = groupBox.title()
            selectedDish = None
            for radioButton in groupBox.radioButtons:
                if radioButton.isChecked():
                    selectedDish = radioButton.text()
                    break
            if selectedDish:
                order[category] = selectedDish

        self.orders.append(order)
        self.saveOrders()
        self.updateOrdersDisplay()

    def deleteOrder(self, index):
        reply = QMessageBox.question(self, 'Подтверждение удаления', 'Вы уверены, что хотите удалить этот заказ?',
                                     QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
                                     QMessageBox.StandardButton.No)

        if reply == QMessageBox.StandardButton.Yes:
            if 0 <= index < len(self.orders):
                del self.orders[index]
                self.saveOrders()
                self.updateOrdersDisplay()

    def resetOrders(self):
        reply = QMessageBox.question(self, 'Подтверждение сброса', 'Вы уверены, что хотите сбросить все заказы?',
                                     QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
                                     QMessageBox.StandardButton.No)

        if reply == QMessageBox.StandardButton.Yes:
            self.orders = []
            self.saveOrders()
            self.updateOrdersDisplay()

    def saveOrders(self):
        with open('orders.json', 'w', encoding='utf-8') as f:
            json.dump(self.orders, f, ensure_ascii=False, indent=4)

    def loadOrders(self):
        if exists('orders.json'):
            with open('orders.json', 'r', encoding='utf-8') as f:
                try:
                    return json.load(f)
                except json.JSONDecodeError:
                    return []
        return []

    def updateOrdersDisplay(self):
        while QLayoutItem := self.ordersLayout.takeAt(0):
            if QLayoutItem.widget():
                QLayoutItem.widget().deleteLater()

        for i, order in enumerate(self.orders, start=1):
            orderFrame = QFrame()
            orderFrame.setFrameShape(QFrame.Shape.StyledPanel)
            orderFrame.setLineWidth(1)
            layout = QVBoxLayout(orderFrame)

            orderLabel = QLabel(f"Заказ #{i}")
            orderLabel.setFont(QFont('Arial', 16, QFont.Weight.Bold))
            layout.addWidget(orderLabel)

            for category, dish in order.items():
                detailLabel = QLabel(f"{category}: {dish}")
                detailLabel.setFont(QFont('Arial', 14))
                layout.addWidget(detailLabel)

            deleteButton = QPushButton('Удалить этот заказ')
            deleteButton.clicked.connect(lambda checked, index=i - 1: self.deleteOrder(index))
            layout.addWidget(deleteButton)

            self.ordersLayout.addWidget(orderFrame)


def main():
    app = QApplication(sys.argv)
    ex = LunchOrderApp()
    ex.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()
