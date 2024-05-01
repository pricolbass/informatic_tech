import sys
import sqlite3
from PyQt6.QtWidgets import (QApplication, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QLineEdit,
                             QListWidget, QLCDNumber, QTabWidget, QMessageBox, QCheckBox, QDialog)
from PyQt6.QtCore import QEvent
import hashlib
from PyQt6.QtGui import QFont, QIcon
from PyQt6.QtCore import Qt
from string import punctuation, ascii_letters


def init_db():
    conn = sqlite3.connect('database')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS users
                 (login TEXT PRIMARY KEY,
                 password TEXT,
                 email TEXT,
                 phone TEXT)''')
    c.execute('''CREATE TABLE IF NOT EXISTS questions
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                 user_login TEXT,
                 question TEXT,
                 decisionMade BOOLEAN,
                 FOREIGN KEY(user_login) REFERENCES users(login))''')
    c.execute('''CREATE TABLE IF NOT EXISTS arguments
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                 question_id INTEGER,
                 argument TEXT,
                 type TEXT,
                 FOREIGN KEY(question_id) REFERENCES questions(id))''')
    conn.commit()
    conn.close()


init_db()


class PasswordLineEdit(QWidget):
    def __init__(self, icon_path, icon_path_toggle, parent=None):
        super().__init__(parent)
        self.line_edit = QLineEdit(self)
        self.toggle_button = QPushButton(self)
        self.toggle_button.setIcon(QIcon(icon_path))
        self.toggle_button.setFixedSize(22, 22)
        self.icon_path = icon_path
        self.icon_path_toggle = icon_path_toggle
        self.toggle_button.pressed.connect(self.toggle_visibility)

        self.line_edit.setEchoMode(QLineEdit.EchoMode.Password)
        layout = QHBoxLayout(self)
        layout.addWidget(self.line_edit, 1)
        layout.addWidget(self.toggle_button)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        self.line_edit.setStyleSheet("""
            QLineEdit {
                border: 1px solid #ccc;
                border-radius: 5px;
                padding: 5px;
            }
        """)
        self.toggle_button.setStyleSheet("QPushButton {border: none; margin: 0; background: transparent;}")

    def toggle_visibility(self):
        if self.line_edit.echoMode() == QLineEdit.EchoMode.Password:
            self.line_edit.setEchoMode(QLineEdit.EchoMode.Normal)
            self.toggle_button.setIcon(QIcon(self.icon_path_toggle))
        else:
            self.line_edit.setEchoMode(QLineEdit.EchoMode.Password)
            self.toggle_button.setIcon(QIcon(self.icon_path))

    def text(self):
        return self.line_edit.text()

    def setText(self, text):
        self.line_edit.setText(text)


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Регистрация и Вход")
        self.setGeometry(100, 100, 300, 400)
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)
        self.initUI()
        self.setStyleSheet("""
                    QWidget {
                        font-family: Arial;
                        font-size: 14px;
                    }
                    QLabel {
                        margin-bottom: 5px;
                    }
                    QLineEdit {
                        padding: 5px;
                        border: 1px solid #ccc;
                        border-radius: 3px;
                        margin-bottom: 10px;
                    }
                    QPushButton {
                        background-color: #007bff;
                        color: white;
                        border: none;
                        padding: 10px 15px;
                        border-radius: 3px;
                        margin-top: 10px;
                    }
                    QPushButton:pressed {
                        background-color: #0056b3;
                    }
                """)

    def initUI(self):
        self.clearLayout(self.layout)

        centerWidget = QWidget()
        centerLayout = QVBoxLayout()
        centerWidget.setLayout(centerLayout)

        self.welcomeLabel = QLabel("Добро пожаловать! Выберите действие:")
        self.welcomeLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.welcomeLabel.setFont(QFont('Arial', 14, QFont.Weight.Bold))

        self.registrationButton = QPushButton("Регистрация")
        self.loginButton = QPushButton("Вход")

        centerLayout.addWidget(self.welcomeLabel, alignment=Qt.AlignmentFlag.AlignHCenter)
        centerLayout.addWidget(self.registrationButton, alignment=Qt.AlignmentFlag.AlignHCenter)
        centerLayout.addWidget(self.loginButton, alignment=Qt.AlignmentFlag.AlignHCenter)

        self.layout.addWidget(centerWidget,
                              alignment=Qt.AlignmentFlag.AlignCenter)

        self.registrationButton.clicked.connect(self.registration)
        self.loginButton.clicked.connect(self.login)

    def clearLayout(self, layout):
        while layout.count():
            child = layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()

    def registration(self):
        self.clearLayout(self.layout)
        self.registrationForm()

    def login(self):
        self.clearLayout(self.layout)
        self.loginForm()

    def registrationForm(self):
        self.usernameLabel = QLabel("Логин:")
        self.usernameEdit = QLineEdit()
        self.passwordLabel = QLabel("Пароль:")
        self.passwordEdit = PasswordLineEdit("eye_icon.png", "eye_slash_icon.png")
        self.layout.addWidget(self.passwordEdit)

        self.emailLabel = QLabel("Email:")
        self.emailEdit = QLineEdit()
        self.phoneLabel = QLabel("Телефон:")
        self.phoneEdit = QLineEdit()
        self.registerButton = QPushButton("Зарегистрироваться")
        self.backButton = QPushButton("Назад")

        self.layout.addWidget(self.usernameLabel)
        self.layout.addWidget(self.usernameEdit)
        self.layout.addWidget(self.passwordLabel)
        self.layout.addWidget(self.passwordEdit)
        self.layout.addWidget(self.emailLabel)
        self.layout.addWidget(self.emailEdit)
        self.layout.addWidget(self.phoneLabel)
        self.layout.addWidget(self.phoneEdit)
        self.layout.addWidget(self.registerButton)
        self.layout.addWidget(self.backButton)

        self.registerButton.clicked.connect(self.performRegistration)
        self.backButton.clicked.connect(self.initUI)

    def loginForm(self):
        self.loginUsernameLabel = QLabel("Логин:")
        self.loginUsernameEdit = QLineEdit()
        self.loginPasswordLabel = QLabel("Пароль:")
        self.loginPasswordEdit = QLineEdit()
        self.loginPasswordEdit = PasswordLineEdit("eye_icon.png", "eye_slash_icon.png")
        self.layout.addWidget(self.loginPasswordEdit)
        self.loginButton = QPushButton("Войти")
        self.backButton = QPushButton("Назад")

        self.layout.addWidget(self.loginUsernameLabel)
        self.layout.addWidget(self.loginUsernameEdit)
        self.layout.addWidget(self.loginPasswordLabel)
        self.layout.addWidget(self.loginPasswordEdit)
        self.layout.addWidget(self.loginButton)
        self.layout.addWidget(self.backButton)

        self.loginButton.clicked.connect(self.performLogin)
        self.backButton.clicked.connect(self.initUI)

    def togglePasswordVisibility(self, passwordEdit):
        if passwordEdit.echoMode() == QLineEdit.EchoMode.Password:
            passwordEdit.setEchoMode(QLineEdit.EchoMode.Normal)
        else:
            passwordEdit.setEchoMode(QLineEdit.EchoMode.Password)

    def performRegistration(self):
        login = self.usernameEdit.text()
        password = self.passwordEdit.text()
        email = self.emailEdit.text()
        phone = self.phoneEdit.text()

        if len(login) < 5 or not all(char in ascii_letters + '0123456789' for char in login):
            QMessageBox.critical(self, "Ошибка",
                                 "Логин должен быть не менее 5 символов и содержать только буквы и цифры.")
            return
        if len(password) < 8 or not any(char.isdigit() for char in password) or not any(
                char.isupper() for char in password) \
                or not any(char.islower() for char in password) or not any(char in punctuation for char in password):
            QMessageBox.critical(self, "Ошибка",
                                 "Пароль должен быть не менее 8 символов, содержать цифры, заглавные и строчные буквы,"
                                 " а также специальные символы.")
            return
        if '@' not in email or email.count('@') > 1 or email.startswith('@') or email.endswith('@'):
            QMessageBox.critical(self, "Ошибка", "Некорректный формат email.")
            return
        if not (phone.startswith('+7') or phone.startswith('8')) or len(phone.strip('+')) != 11:
            QMessageBox.critical(self, "Ошибка", "Телефон должен начинаться на +7 или 8 и содержать 11 цифр.")
            return
        if self.user_exists(login, email, phone):
            QMessageBox.critical(self, "Ошибка", "Пользователь с такими данными уже существует.")
            return

        self.save_user(login, password, email, phone)
        QMessageBox.information(self, "Успех", "Вы успешно зарегистрированы!")
        self.initUI()

    def performLogin(self):
        login = self.loginUsernameEdit.text()
        password = self.loginPasswordEdit.text()
        conn = sqlite3.connect('database')
        c = conn.cursor()
        c.execute('SELECT password FROM users WHERE login=?', (login,))
        user_data = c.fetchone()
        conn.close()
        if user_data and user_data[0] == self.hash_password(password):
            QMessageBox.information(self, "Успех", "Авторизация успешна. Добро пожаловать!")
            self.hide()
            self.openDecisionHelper(login)
        else:
            QMessageBox.critical(self, "Ошибка", "Логин или пароль неверны.")

    def openDecisionHelper(self, user_login):
        self.decisionHelper = DecisionHelper(user_login)
        self.decisionHelper.show()

    def save_user(self, login, password, email, phone):
        conn = sqlite3.connect('database')
        c = conn.cursor()
        c.execute('INSERT INTO users (login, password, email, phone) VALUES (?, ?, ?, ?)',
                  (login, self.hash_password(password), email, phone))
        conn.commit()
        conn.close()

    def hash_password(self, password):
        return hashlib.sha256(password.encode()).hexdigest()

    def user_exists(self, login, email, phone):
        conn = sqlite3.connect('database')
        c = conn.cursor()
        c.execute('SELECT * FROM users WHERE login=? OR email=? OR phone=?', (login, email, phone))
        user = c.fetchone()
        conn.close()
        return bool(user)


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
        if not self.parent().questions[self.parent().currentQuestion]["decisionMade"]:
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
    def __init__(self, user_login):
        super().__init__()
        self.user_login = user_login
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

        self.editQuestionButton = QPushButton('Изменить вопрос')
        self.editQuestionButton.clicked.connect(self.editCurrentQuestion)
        self.layout.addWidget(self.editQuestionButton)

        self.deleteQuestionButton = QPushButton('Удалить вопрос')
        self.deleteQuestionButton.clicked.connect(self.deleteCurrentQuestion)

        questionButtonsLayout = QHBoxLayout()
        questionButtonsLayout.addWidget(self.editQuestionButton)
        questionButtonsLayout.addWidget(self.deleteQuestionButton)

        self.layout.addLayout(questionButtonsLayout)

        self.tabWidget = QTabWidget()
        self.tabWidget.currentChanged.connect(self.changeQuestion)
        self.layout.addWidget(self.tabWidget)

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

        self.decisionMadeCheckbox = QCheckBox("Решение принято")
        self.decisionMadeCheckbox.stateChanged.connect(self.toggleDecisionState)
        self.layout.addWidget(self.decisionMadeCheckbox)

        self.resetButton = QPushButton('Сброс')
        self.resetButton.clicked.connect(self.resetCounts)
        self.layout.addWidget(self.resetButton)

        self.moveProToConButton = QPushButton('-->')
        self.moveProToConButton.clicked.connect(lambda: self.moveArgumentBetweenLists('pro', 'con'))
        self.moveConToProButton = QPushButton('<--')
        self.moveConToProButton.clicked.connect(lambda: self.moveArgumentBetweenLists('con', 'pro'))

        moveButtonsLayout = QVBoxLayout()
        moveButtonsLayout.addWidget(self.moveProToConButton)
        moveButtonsLayout.addWidget(self.moveConToProButton)

        argumentsLayout.insertLayout(1, moveButtonsLayout)

    def loadData(self):
        conn = sqlite3.connect('database')
        c = conn.cursor()

        self.questions = {}

        c.execute('SELECT id, question, decisionMade FROM questions WHERE user_login=?', (self.user_login,))
        questions = c.fetchall()

        for question_id, question_text, decision_made in questions:
            if question_text not in self.questions:
                self.questions[question_text] = {"pro": [], "con": [], "decisionMade": bool(decision_made)}

            c.execute('SELECT argument, type FROM arguments WHERE question_id=?', (question_id,))
            arguments = c.fetchall()

            for argument_text, argument_type in arguments:
                self.questions[question_text][argument_type].append(argument_text)

            if not self.tabWidget.findChild(QWidget, name=question_text):
                tab = QWidget()
                tab.setObjectName(question_text)
                self.tabWidget.addTab(tab, question_text)

        self.changeQuestion()
        conn.close()

    def saveData(self):
        conn = sqlite3.connect('database')
        c = conn.cursor()
        for question, details in self.questions.items():
            c.execute('SELECT id FROM questions WHERE question=? AND user_login=?', (question, self.user_login))
            question_id = c.fetchone()
            if question_id:
                question_id = question_id[0]
                c.execute('UPDATE questions SET decisionMade=? WHERE id=?', (details["decisionMade"], question_id))
            else:
                c.execute('INSERT INTO questions (user_login, question, decisionMade) VALUES (?, ?, ?)',
                          (self.user_login, question, details["decisionMade"]))
                question_id = c.lastrowid
            c.execute('DELETE FROM arguments WHERE question_id=?', (question_id,))
            for arg in details["pro"]:
                c.execute('INSERT INTO arguments (question_id, argument, type) VALUES (?, ?, ?)',
                          (question_id, arg, 'pro'))
            for arg in details["con"]:
                c.execute('INSERT INTO arguments (question_id, argument, type) VALUES (?, ?, ?)',
                          (question_id, arg, 'con'))
        conn.commit()
        conn.close()

    def addQuestion(self):
        question = self.questionInput.text()
        if question and question not in self.questions:
            self.questions[question] = {"pro": [], "con": [], "decisionMade": False}
            tab = QWidget()
            tab.setObjectName(question)
            self.tabWidget.addTab(tab, question)
            self.questionInput.clear()
            self.saveData()

    def changeQuestion(self):
        currentIndex = self.tabWidget.currentIndex()
        if currentIndex != -1:
            self.currentQuestion = self.tabWidget.tabText(currentIndex)
        else:
            self.currentQuestion = ""
        self.questionDisplay.setText(f"Текущий вопрос: {self.currentQuestion}")
        self.updateUIState()
        self.updateArgumentsDisplay()

    def editCurrentQuestion(self):
        dialog = QDialog(self)
        dialog.setWindowTitle("Изменить вопрос")
        layout = QVBoxLayout()
        newQuestionInput = QLineEdit(self.currentQuestion)
        layout.addWidget(newQuestionInput)
        saveButton = QPushButton("Сохранить")
        saveButton.clicked.connect(lambda: self.updateQuestion(newQuestionInput.text()))
        layout.addWidget(saveButton)
        dialog.setLayout(layout)
        dialog.exec()

    def updateQuestion(self, newQuestionText):
        if newQuestionText and newQuestionText != self.currentQuestion:
            conn = sqlite3.connect('database')
            c = conn.cursor()

            c.execute('SELECT question FROM questions WHERE user_login=? AND question=?',
                      (self.user_login, newQuestionText))
            if c.fetchone():
                QMessageBox.critical(self, "Ошибка", "Такой вопрос уже существует.")
                return

            c.execute('UPDATE questions SET question=? WHERE question=? AND user_login=?',
                      (newQuestionText, self.currentQuestion, self.user_login))
            conn.commit()

            question_data = self.questions.pop(self.currentQuestion)
            self.questions[newQuestionText] = question_data

            index = self.tabWidget.indexOf(self.tabWidget.findChild(QWidget, name=self.currentQuestion))
            if index != -1:
                tab = self.tabWidget.widget(index)
                if tab:
                    tab.setObjectName(newQuestionText)
                    self.tabWidget.setTabText(index, newQuestionText)

            self.currentQuestion = newQuestionText
            self.questionDisplay.setText(f"Текущий вопрос: {self.currentQuestion}")
            self.updateUIState()
            self.updateArgumentsDisplay()

            conn.close()

    def deleteCurrentQuestion(self):
        if self.currentQuestion:
            reply = QMessageBox.question(self, 'Удаление вопроса',
                                         f"Вы действительно хотите удалить вопрос \"{self.currentQuestion}\"?",
                                         QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
                                         QMessageBox.StandardButton.No)

            if reply == QMessageBox.StandardButton.Yes:
                conn = sqlite3.connect('database')
                c = conn.cursor()

                c.execute('SELECT id FROM questions WHERE question=? AND user_login=?',
                          (self.currentQuestion, self.user_login))
                question_id = c.fetchone()

                if question_id:
                    question_id = question_id[0]

                    c.execute('DELETE FROM arguments WHERE question_id=?', (question_id,))

                    c.execute('DELETE FROM questions WHERE id=?', (question_id,))
                    conn.commit()

                conn.close()

                if self.currentQuestion in self.questions:
                    self.questions.pop(self.currentQuestion)

                currentIndex = self.tabWidget.currentIndex()
                if currentIndex != -1:
                    self.tabWidget.removeTab(currentIndex)

                self.changeQuestion()

    def addArgument(self, listType):
        argument = self.argumentInput.text()
        if argument and not self.questions[self.currentQuestion]["decisionMade"]:
            self.questions[self.currentQuestion][listType].append(argument)
            self.argumentInput.clear()
            self.updateArgumentsDisplay()
            self.saveData()

    def deleteArgument(self, listType, argumentText):
        if self.currentQuestion and not self.questions[self.currentQuestion]["decisionMade"]:
            conn = sqlite3.connect('database')
            c = conn.cursor()

            c.execute('SELECT id FROM questions WHERE question=? AND user_login=?',
                      (self.currentQuestion, self.user_login))
            question_id = c.fetchone()

            if question_id:
                question_id = question_id[0]

                c.execute('DELETE FROM arguments WHERE question_id=? AND argument=? AND type=?',
                          (question_id, argumentText, listType))
                conn.commit()

                self.questions[self.currentQuestion][listType] = [
                    arg for arg in self.questions[self.currentQuestion][listType] if arg != argumentText]
                self.updateArgumentsDisplay()

            conn.close()
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
        if self.currentQuestion and not self.questions[self.currentQuestion]["decisionMade"]:
            self.questions[self.currentQuestion]["pro"] = []
            self.questions[self.currentQuestion]["con"] = []
            self.updateArgumentsDisplay()
            self.saveData()

    def updateArgumentsOrder(self, listType):
        if not self.questions[self.currentQuestion]["decisionMade"]:
            newOrder = [self.proArgumentsList.item(i).text() for i in
                        range(self.proArgumentsList.count())] if listType == "pro" else [
                self.conArgumentsList.item(i).text() for i in range(self.conArgumentsList.count())]
            self.questions[self.currentQuestion][listType] = newOrder
            self.saveData()

    def moveArgumentBetweenLists(self, fromList, toList):
        if fromList == toList:
            return

        currentRow = self.proArgumentsList.currentRow() if fromList == 'pro' else self.conArgumentsList.currentRow()
        if currentRow != -1:
            argument = self.proArgumentsList.currentItem().text() if fromList == 'pro' else self.conArgumentsList.currentItem().text()
            if fromList == 'pro':
                self.proArgumentsList.takeItem(currentRow)
                self.conArgumentsList.addItem(argument)
            else:
                self.conArgumentsList.takeItem(currentRow)
                self.proArgumentsList.addItem(argument)
            self.moveArgument(fromList, toList, argument)
            self.updateLCDNumbers()

    def moveArgument(self, fromList, toList, argument):
        self.questions[self.currentQuestion][fromList].remove(argument)
        self.questions[self.currentQuestion][toList].append(argument)
        self.saveData()

    def toggleDecisionState(self, state):
        if self.currentQuestion:
            self.questions[self.currentQuestion]["decisionMade"] = state == 2
            self.updateUIState()
            self.saveData()

    def updateUIState(self):
        decisionMade = self.questions.get(self.currentQuestion, {}).get("decisionMade", False)
        self.decisionMadeCheckbox.setChecked(decisionMade)
        self.addProArgumentButton.setEnabled(not decisionMade)
        self.addConArgumentButton.setEnabled(not decisionMade)
        self.argumentInput.setEnabled(not decisionMade)
        self.proArgumentsList.setDragEnabled(not decisionMade)
        self.conArgumentsList.setDragEnabled(not decisionMade)
        self.resetButton.setEnabled(not decisionMade)
        self.moveProToConButton.setEnabled(not decisionMade)
        self.moveConToProButton.setEnabled(not decisionMade)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    loginWindow = MainWindow()
    loginWindow.show()
    sys.exit(app.exec())
