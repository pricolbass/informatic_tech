import sys
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QLineEdit, QCalendarWidget, QTimeEdit, \
    QListWidget, QMainWindow
from PyQt6 import uic
import json


class DiaryApp(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('design_plan.ui', self)
        self.initUI()
        self.loadEvents()

    def initUI(self):
        self.setWindowTitle('Ежедневник')

        self.centralWidget = self.findChild(QWidget, 'centralwidget')
        self.layout = self.findChild(QVBoxLayout, 'layout')


        self.calendar = self.findChild(QCalendarWidget, 'calendar')
        self.timeEdit = self.findChild(QTimeEdit, 'timeEdit')
        self.eventInput = self.findChild(QLineEdit, 'eventInput')
        self.addButton = self.findChild(QPushButton, 'addButton')
        self.eventList = self.findChild(QListWidget, 'eventList')

        self.addButton.clicked.connect(self.addEvent)
        self.eventList.itemDoubleClicked.connect(self.removeEvent)


    def addEvent(self):
        event_date = self.calendar.selectedDate().toString("yyyy-MM-dd")
        event_time = self.timeEdit.time().toString("HH:mm")
        event_name = self.eventInput.text()
        if event_name:
            event_str = f"{event_date} {event_time} - {event_name}"
            self.eventList.addItem(event_str)
            self.eventInput.clear()
            self.saveEvents()

    def removeEvent(self, item):
        self.eventList.takeItem(self.eventList.row(item))
        self.saveEvents()

    def saveEvents(self):
        events = [self.eventList.item(i).text() for i in range(self.eventList.count())]
        with open("events.json", "w") as file:
            json.dump(events, file)

    def loadEvents(self):
        try:
            with open("events.json", "r") as file:
                events = json.load(file)
                self.eventList.addItems(events)
        except FileNotFoundError:
            pass


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = DiaryApp()
    window.show()
    sys.exit(app.exec())
