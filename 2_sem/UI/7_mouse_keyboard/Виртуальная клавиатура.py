import sys
import sqlite3
from PyQt6.QtWidgets import (QApplication, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QLineEdit,
                             QListWidget, QLCDNumber, QTabWidget, QMessageBox, QCheckBox, QDialog, QMenu, QInputDialog,
                             QMenuBar, QMenu, QFileDialog)
from PyQt6.QtCore import QEvent
import hashlib
from PyQt6.QtGui import QFont, QIcon, QAction, QShortcut, QKeySequence
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


class CustomTabWidget(QTabWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.RightButton:
            tabIndex = self.tabBar().tabAt(
                event.position().toPoint())
            if tabIndex != -1:
                self.showContextMenu(tabIndex,
                                     event.globalPosition().toPoint())

        super().mousePressEvent(event)

    def showContextMenu(self, tabIndex, globalPos):
        contextMenu = QMenu(self)
        renameAction = contextMenu.addAction("Переименовать")
        deleteAction = contextMenu.addAction("Удалить")

        action = contextMenu.exec(globalPos)

        if action == renameAction:
            self.renameTab(tabIndex)
        elif action == deleteAction:
            self.deleteTab(tabIndex)

    def renameTab(self, tabIndex):
        dialog = QDialog(self)
        dialog.setWindowTitle("Переименовать вкладку")
        layout = QVBoxLayout()
        newNameLineEdit = QLineEdit(self.tabText(tabIndex))
        layout.addWidget(newNameLineEdit)
        saveButton = QPushButton("Сохранить")
        saveButton.clicked.connect(lambda: self.updateTabName(tabIndex, newNameLineEdit.text(), dialog))
        layout.addWidget(saveButton)
        dialog.setLayout(layout)
        dialog.exec()

    def updateTabName(self, tabIndex, newName, dialog):
        if newName:
            oldName = self.tabText(tabIndex)
            self.setTabText(tabIndex, newName)
            if oldName in self.parent().questions:
                conn = sqlite3.connect('database')
                c = conn.cursor()
                try:
                    c.execute("UPDATE questions SET question=? WHERE question=? AND user_login=?",
                              (newName, oldName, self.parent().user_login))
                    conn.commit()
                except sqlite3.Error as e:
                    print(f"An error occurred: {e.args[0]}")
                finally:
                    conn.close()
                question_data = self.parent().questions.pop(oldName)
                self.parent().questions[newName] = question_data
                self.parent().changeQuestion()
            dialog.accept()

    def deleteTab(self, tabIndex):
        questionName = self.tabText(tabIndex)
        reply = QMessageBox.question(self, 'Удаление вопроса',
                                     "Вы действительно хотите удалить эту вкладку?",
                                     QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
                                     QMessageBox.StandardButton.No)
        if reply == QMessageBox.StandardButton.Yes:
            question_data = self.parent().questions[questionName]
            self.removeTab(tabIndex)
            self.deleteQuestionFromDatabase(questionName)

    def deleteQuestionFromDatabase(self, questionName):
        conn = sqlite3.connect('database')
        c = conn.cursor()
        c.execute("DELETE FROM questions WHERE question=?", (questionName,))
        c.execute("DELETE FROM arguments WHERE question_id NOT IN (SELECT id FROM questions)")
        conn.commit()
        conn.close()


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
        self.passwordEdit = PasswordLineEdit("eye_slash_icon.png", "eye_icon.png")
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
        self.loginPasswordEdit = PasswordLineEdit("eye_slash_icon.png", "eye_icon.png")
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
        self.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.customContextMenuRequested.connect(self.showContextMenu)

    def showContextMenu(self, position):
        contextMenu = QMenu(self)

        renameAction = contextMenu.addAction("Переименовать аргумент")
        deleteAction = contextMenu.addAction("Удалить аргумент")

        action = contextMenu.exec(self.mapToGlobal(position))

        if action == deleteAction:
            self.deleteArgument()
        elif action == renameAction:
            self.renameArgument()

    def deleteArgument(self):
        currentItem = self.currentItem()
        if currentItem is not None:
            reply = QMessageBox.question(self, 'Удаление аргумента',
                                         "Вы действительно хотите удалить этот аргумент?",
                                         QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
                                         QMessageBox.StandardButton.No)
            if reply == QMessageBox.StandardButton.Yes:
                argumentText = currentItem.text()
                self.takeItem(self.currentRow())
                self.parent().deleteArgument(self.listType, argumentText)

    def renameArgument(self):
        currentItem = self.currentItem()
        if currentItem is not None:
            row = self.currentRow()
            oldArgumentText = currentItem.text()

            text, ok = QInputDialog.getText(self, 'Переименовать аргумент', 'Введите новое название аргумента:',
                                            QLineEdit.EchoMode.Normal, oldArgumentText)
            if ok and text:
                currentItem.setText(text)
                self.updateArgumentInDatabase(oldArgumentText, text)
                self.parent().undo_stack.append(("rename_argument", [self.listType, row, oldArgumentText, text], {}))

    def updateArgumentInDatabase(self, oldText, newText):
        conn = sqlite3.connect('database')
        c = conn.cursor()

        c.execute('SELECT id FROM questions WHERE question=? AND user_login=?',
                  (self.parent().currentQuestion, self.parent().user_login))
        question_id = c.fetchone()

        if question_id:
            c.execute("UPDATE arguments SET argument=? WHERE question_id=? AND argument=? AND type=?",
                      (newText, question_id[0], oldText, self.listType))
            conn.commit()
            conn.close()

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
        self.undo_stack = []
        self.redo_stack = []
        self.initUI()
        self.setupMenuBar()
        self.setupShortcuts()
        self.loadData()

    def setupMenuBar(self):
        menuBar = QMenuBar()

        fileMenu = menuBar.addMenu('Файл')
        createAct = QAction('Создать', self)
        createAct.setShortcut('Ctrl+F')
        fileMenu.addAction(createAct)

        openAct = QAction('Открыть...', self)
        openAct.setShortcut('Ctrl+O')
        fileMenu.addAction(openAct)

        saveAct = QAction('Сохранить', self)
        saveAct.setShortcut('Ctrl+S')
        fileMenu.addAction(saveAct)

        saveAsAct = QAction('Сохранить как...', self)
        saveAsAct.setShortcut('Ctrl+Shift+S')
        fileMenu.addAction(saveAsAct)

        exitAct = QAction('Выход', self)
        fileMenu.addAction(exitAct)

        createAct.triggered.connect(self.createDocument)
        openAct.triggered.connect(self.openDocument)
        saveAct.triggered.connect(self.saveDocument)
        saveAsAct.triggered.connect(self.saveDocumentAs)
        exitAct.triggered.connect(self.exitApplication)

        self.layout.setMenuBar(menuBar)

    def setupShortcuts(self):
        QShortcut(QKeySequence('F1'), self).activated.connect(self.showHelp)
        QShortcut(QKeySequence('Ctrl+N'), self).activated.connect(self.addQuestion)
        QShortcut(QKeySequence('Ctrl+Del'), self).activated.connect(self.deleteCurrentQuestion)
        QShortcut(QKeySequence('Ctrl+Z'), self).activated.connect(self.undoLastAction)
        QShortcut(QKeySequence('Del'), self).activated.connect(self.deleteSelectedArgument)

    def showHelp(self):
        help_text = """
        Добро пожаловать в приложение «Помощник по принятию решений»! Вот как использовать это приложение:

        - F1: отобразить это справочное сообщение.
        - Ctrl+N: добавить новый вопрос/вкладку.
        - Ctrl+Del: удалить текущий выбранный вопрос/вкладку.
        - Ctrl+Z: отменить последнее действие.
        - Del: удалить выбранный аргумент после подтверждения.

        Перемещайтесь по вопросам с помощью вкладок и при необходимости добавляйте аргументы за или против каждого вопроса.
        """
        QMessageBox.information(self, "Help", help_text)

    def undoLastAction(self):
        if self.undo_stack:
            action, args, kwargs = self.undo_stack.pop()
            undo_function = getattr(self, f"undo_{action}")
            undo_function(*args, **kwargs)
            self.redo_stack.append((action, args, kwargs))
            self.saveData()

    def undo_add_question(self, question_text, question_data):
        self.questions.pop(question_text)
        index = self.tabWidget.indexOf(self.tabWidget.findChild(QWidget, name=question_text))
        if index != -1:
            self.tabWidget.removeTab(index)

        conn = sqlite3.connect('database')
        c = conn.cursor()
        try:
            c.execute('DELETE FROM questions WHERE user_login=? AND question=?',
                      (self.user_login, question_text))
            conn.commit()
        except sqlite3.Error as e:
            print(f"An error occurred: {e.args[0]}")
        finally:
            conn.close()

        if self.questions:
            self.currentQuestion = next(iter(self.questions))
            self.tabWidget.setCurrentIndex(0)
        else:
            self.currentQuestion = None
        self.updateUIState()

    def undo_update_question(self, old_question_text, new_question_text, question_data):
        self.questions.pop(new_question_text)
        self.questions[old_question_text] = question_data

        conn = sqlite3.connect('database')
        c = conn.cursor()

        c.execute('SELECT question FROM questions WHERE user_login=? AND question=?',
                  (self.user_login, old_question_text))
        if c.fetchone():
            QMessageBox.critical(self, "Ошибка", "Такой вопрос уже существует.")
            return

        c.execute('UPDATE questions SET question=? WHERE question=? AND user_login=?',
                  (old_question_text, self.currentQuestion, self.user_login))
        conn.commit()

        index = self.tabWidget.indexOf(self.tabWidget.findChild(QWidget, name=new_question_text))
        if index != -1:
            tab = self.tabWidget.widget(index)
            if tab:
                tab.setObjectName(old_question_text)
                self.tabWidget.setTabText(index, old_question_text)

        self.currentQuestion = old_question_text
        self.updateUIState()
        self.updateArgumentsDisplay()
        self.changeQuestion()

    def undo_delete_question(self, question_text, question_data):
        self.questions[question_text] = question_data
        tab = QWidget()
        tab.setObjectName(question_text)
        self.tabWidget.addTab(tab, question_text)
        self.tabWidget.currentChanged.connect(self.changeQuestion)
        self.currentQuestion = question_text
        index = self.tabWidget.indexOf(self.tabWidget.findChild(QWidget, name=question_text))
        self.tabWidget.setCurrentIndex(index)
        self.updateUIState()
        self.updateArgumentsDisplay()

    def undo_toggle_decision_state(self, question_text, old_decision_state):
        if self.currentQuestion == question_text:
            self.questions[question_text]["decisionMade"] = old_decision_state
            self.updateUIState()

    def undo_add_argument(self, list_type, argument):
        self.questions[self.currentQuestion][list_type].remove(argument)
        self.updateArgumentsDisplay()

    def undo_rename_argument(self, list_type, row, old_text, new_text):
        if self.currentQuestion:
            arguments_list = self.proArgumentsList if list_type == "pro" else self.conArgumentsList
            item = arguments_list.item(row)
            if item:
                item.setText(old_text)
                arguments_list.updateArgumentInDatabase(new_text, old_text)

    def undo_delete_argument(self, list_type, argument):
        self.questions[self.currentQuestion][list_type].append(argument)
        self.updateArgumentsDisplay()

    def undo_move_argument(self, from_list, to_list, argument):
        self.questions[self.currentQuestion][to_list].remove(argument)
        self.questions[self.currentQuestion][from_list].append(argument)
        self.updateArgumentsDisplay()

    def undo_reset_counts(self, pro_arguments, con_arguments):
        self.questions[self.currentQuestion]["pro"] = pro_arguments
        self.questions[self.currentQuestion]["con"] = con_arguments
        self.updateArgumentsDisplay()

    def deleteSelectedArgument(self):
        pro_selected_items = self.proArgumentsList.selectedItems()
        con_selected_items = self.conArgumentsList.selectedItems()

        if pro_selected_items:
            selected_item = pro_selected_items[0]
            argument_text = selected_item.text()
            list_type = "pro"
        elif con_selected_items:
            selected_item = con_selected_items[0]
            argument_text = selected_item.text()
            list_type = "con"
        else:
            return

        reply = QMessageBox.question(self, 'Delete Argument',
                                     "Вы уверены, что хотите удалить выбранный аргумент?",
                                     QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        if reply == QMessageBox.StandardButton.Yes:
            self.deleteArgument(list_type, argument_text)

    def createDocument(self):
        reply = QMessageBox.question(self, 'Создать новый файл',
                                     "Вы уверены, что хотите создать новый файл? Это удалит все ваши вопросы и аргументы.",
                                     QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
                                     QMessageBox.StandardButton.No)
        if reply == QMessageBox.StandardButton.Yes:
            conn = sqlite3.connect('database')
            c = conn.cursor()
            try:
                c.execute('DELETE FROM arguments WHERE question_id IN (SELECT id FROM questions WHERE user_login=?)',
                          (self.user_login,))
                c.execute('DELETE FROM questions WHERE user_login=?', (self.user_login,))
                conn.commit()
                QMessageBox.information(self, 'Сброс завершен', 'Все ваши вопросы и аргументы были удалены.')
            except sqlite3.Error as e:
                QMessageBox.critical(self, 'Ошибка', f'Произошла ошибка при удалении данных: {e}')
            finally:
                conn.close()

            self.tabWidget.blockSignals(True)
            self.tabWidget.clear()
            self.tabWidget.blockSignals(False)

            self.questions = {}
            self.currentQuestion = ""

            self.updateArgumentsDisplay()
            self.updateUIState()
            self.changeQuestion()
            self.proLCDNumber.display(0)
            self.conLCDNumber.display(0)

    def openDocument(self):
        filename, _ = QFileDialog.getOpenFileName(self, "Открыть базу данных", "",
                                                  "SQLite Files (*.sqlite *.db);;All Files (*)")
        if filename:
            self.importData(filename)

    def importData(self, new_db_path):
        new_conn = sqlite3.connect(new_db_path)
        new_cursor = new_conn.cursor()

        current_conn = sqlite3.connect('database')
        current_cursor = current_conn.cursor()

        try:
            new_cursor.execute("SELECT * FROM questions")
            questions = new_cursor.fetchall()
            new_cursor.execute("SELECT * FROM arguments")
            arguments = new_cursor.fetchall()

            for question in questions:
                current_cursor.execute("SELECT id FROM questions WHERE user_login=? AND question=?",
                                       (self.user_login, question[2]))
                existing_question = current_cursor.fetchone()
                if not existing_question:
                    current_cursor.execute(
                        "INSERT INTO questions (user_login, question, decisionMade) VALUES (?, ?, ?)",
                        (self.user_login, question[2], question[3]))
                    question_id = current_cursor.lastrowid
                else:
                    question_id = existing_question[0]

                related_args = [arg for arg in arguments if arg[1] == question[0]]
                for arg in related_args:
                    current_cursor.execute("SELECT id FROM arguments WHERE question_id=? AND argument=? AND type=?",
                                           (question_id, arg[2], arg[3]))
                    if not current_cursor.fetchone():
                        current_cursor.execute("INSERT INTO arguments (question_id, argument, type) VALUES (?, ?, ?)",
                                               (question_id, arg[2], arg[3]))

            current_conn.commit()
            QMessageBox.information(self, 'Import Successful', 'Questions and arguments imported successfully.')

        except sqlite3.Error as e:
            QMessageBox.critical(self, 'Database Error', f'An error occurred: {e}')
            current_conn.rollback()

        finally:
            new_conn.close()
            current_conn.close()

        self.loadData()
        self.currentQuestion = list(self.questions.keys())[0] if self.questions else None
        self.updateTabs()
        self.updateUIState()

    def saveDocument(self):
        self.saveData()

    def saveDocumentAs(self):
        filename, _ = QFileDialog.getSaveFileName(self, "Сохранить базу данных как", "",
                                                  "SQLite Files (*.sqlite *.db);;All Files (*)")
        if filename:
            if self.makeDatabaseCopy(filename):
                QMessageBox.information(self, 'Database Saved', f'Database saved as {filename}')
            else:
                QMessageBox.critical(self, 'Save Error', 'Failed to save the database.')

    def check_table_exists(self, conn, table_name):
        cursor = conn.cursor()
        cursor.execute(f"SELECT count(name) FROM sqlite_master WHERE type='table' AND name='{table_name}'")
        if cursor.fetchone()[0] == 1:
            return True
        else:
            return False

    def makeDatabaseCopy(self, new_path):
        try:
            old_conn = sqlite3.connect('database')
            old_cur = old_conn.cursor()

            new_conn = sqlite3.connect(new_path)
            new_cur = new_conn.cursor()

            for table_name in ['questions', 'arguments']:
                old_cur.execute(f"SELECT name FROM sqlite_master WHERE type='table' AND name='{table_name}'")
                if not old_cur.fetchone():
                    QMessageBox.critical(None, 'Database Error',
                                         f'Table "{table_name}" does not exist in the source database.')
                    return False

                old_cur.execute(f"SELECT sql FROM sqlite_master WHERE type='table' AND name='{table_name}'")
                create_table_sql = old_cur.fetchone()[0]
                new_cur.execute(create_table_sql)

                old_cur.execute(f"SELECT * FROM {table_name}")
                rows = old_cur.fetchall()
                if rows:
                    cols = len(rows[0])
                    placeholders = ', '.join(['?'] * cols)
                    new_cur.executemany(f"INSERT INTO {table_name} VALUES ({placeholders})", rows)

            new_conn.commit()
        except sqlite3.Error as e:
            QMessageBox.critical(None, 'Database Error', f'An error occurred: {e}')
            new_conn.rollback()
            return False
        finally:
            old_conn.close()
            new_conn.close()

        return True

    def exitApplication(self):
        self.close()

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

        self.tabWidget = CustomTabWidget(self)
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
            try:
                self.questions[question] = {"pro": [], "con": [], "decisionMade": False}
                tab = QWidget()
                tab.setObjectName(question)
                self.tabWidget.addTab(tab, question)
                self.questionInput.clear()
                self.saveData()
                self.undo_stack.append(("add_question", [question], {"question_data": self.questions[question].copy()}))
            except Exception as e:
                QMessageBox.critical(self, "Ошибка", f"Произошла ошибка при добавлении вопроса: {str(e)}")

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

            old_text = self.currentQuestion
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
            self.undo_stack.append(
                ("update_question", [old_text, newQuestionText], {"question_data": question_data.copy()}))
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
                    question_data = self.questions.pop(self.currentQuestion, None)
                    self.undo_stack.append(
                        ("delete_question", [self.currentQuestion], {"question_data": question_data}))

                currentIndex = self.tabWidget.currentIndex()
                if currentIndex != -1:
                    self.tabWidget.removeTab(currentIndex)

                self.changeQuestion()

    def updateTabs(self):
        self.tabWidget.blockSignals(True)
        self.tabWidget.clear()

        for question_id, question_info in self.questions.items():
            tab = QWidget()
            self.tabWidget.addTab(tab, question_id)

        self.tabWidget.blockSignals(False)

        if self.questions:
            self.currentQuestion = next(iter(self.questions))
            self.tabWidget.setCurrentIndex(0)
            self.updateArgumentsDisplay()
        else:
            self.currentQuestion = None

        self.updateUIState()

    def addArgument(self, listType):
        argument = self.argumentInput.text()
        if not self.currentQuestion or self.currentQuestion not in self.questions:
            QMessageBox.warning(self, "No Question Selected", "Пожалуйста, сначала добавьте вопрос, потом аргумент.")
            return
        else:
            if argument and not self.questions[self.currentQuestion]["decisionMade"]:
                conn = sqlite3.connect('database')
                c = conn.cursor()
                try:
                    c.execute("SELECT id FROM questions WHERE question=?", (self.currentQuestion,))
                    question_id = c.fetchone()
                    if question_id:
                        question_id = question_id[0]
                        c.execute("INSERT INTO arguments (question_id, argument, type) VALUES (?, ?, ?)",
                                  (question_id, argument, listType))
                        conn.commit()

                        self.undo_stack.append(("add_argument", [listType, argument], {}))
                        self.questions[self.currentQuestion][listType].append(argument)

                        self.argumentInput.clear()
                        self.updateArgumentsDisplay()
                except sqlite3.Error as e:
                    QMessageBox.critical(self, 'Ошибка', f'Не удалось добавить аргумент: {e}')
                finally:
                    conn.close()

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
                self.undo_stack.append(("delete_argument", [listType, argumentText], {}))

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
        self.proArgumentsList.update()
        self.conArgumentsList.update()
        self.updateLCDNumbers()

    def updateLCDNumbers(self):
        if self.currentQuestion:
            self.proLCDNumber.display(len(self.questions[self.currentQuestion]["pro"]))
            self.conLCDNumber.display(len(self.questions[self.currentQuestion]["con"]))

    def resetCounts(self):
        if self.currentQuestion and not self.questions[self.currentQuestion]["decisionMade"]:
            reply = QMessageBox.question(self, 'Сброс аргументов',
                                         "Вы уверены, что хотите сбросить все аргументы для текущего вопроса?",
                                         QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
                                         QMessageBox.StandardButton.No)

            if reply == QMessageBox.StandardButton.Yes:
                pro_arguments = self.questions[self.currentQuestion]["pro"].copy()
                con_arguments = self.questions[self.currentQuestion]["con"].copy()
                self.questions[self.currentQuestion]["pro"] = []
                self.questions[self.currentQuestion]["con"] = []
                self.updateArgumentsDisplay()

                conn = sqlite3.connect('database')
                c = conn.cursor()
                try:
                    c.execute('SELECT id FROM questions WHERE question=? AND user_login=?',
                              (self.currentQuestion, self.user_login))
                    question_id = c.fetchone()

                    if question_id:
                        c.execute('DELETE FROM arguments WHERE question_id=?', (question_id[0],))
                        conn.commit()
                except sqlite3.Error as e:
                    print(f"An error occurred: {e.args[0]}")
                finally:
                    conn.close()

                self.saveData()

                self.undo_stack.append(
                    ("reset_counts", [], {"pro_arguments": pro_arguments, "con_arguments": con_arguments}))

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

            reply = QMessageBox.question(self, 'Перемещение аргумента',
                                         f"Вы уверены, что хотите переместить аргумент \"{argument}\" из списка \"{fromList}\" в список \"{toList}\"?",
                                         QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
                                         QMessageBox.StandardButton.No)

            if reply == QMessageBox.StandardButton.Yes:
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
        self.undo_stack.append(("move_argument", [fromList, toList, argument], {}))

    def toggleDecisionState(self, state):
        if self.currentQuestion:
            self.questions[self.currentQuestion]["decisionMade"] = state == 2
            self.updateUIState()
            self.saveData()
            old_decision_state = not self.questions[self.currentQuestion]["decisionMade"]
            self.undo_stack.append(
                ("toggle_decision_state", [self.currentQuestion], {"old_decision_state": old_decision_state}))

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
