import sys
import json
import hashlib
from PyQt6.QtWidgets import (QLineEdit, QPushButton, QHBoxLayout, QApplication, QWidget, QVBoxLayout,
                             QLabel, QMessageBox)
from PyQt6.QtGui import QFont, QIcon
from PyQt6.QtCore import Qt
from string import punctuation, ascii_letters


def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()


def user_exists(login, email, phone):
    try:
        with open('database.json', 'r', encoding='utf-8') as file:
            users = json.load(file)
            for user in users:
                if user['login'] == login or user['email'] == email or user['phone'] == phone:
                    return True
    except FileNotFoundError:
        return False
    return False


def save_user(user_data):
    try:
        with open('database.json', 'r', encoding='utf-8') as file:
            users = json.load(file)
    except FileNotFoundError:
        users = []
    users.append(user_data)
    with open('database.json', 'w', encoding='utf-8') as file:
        json.dump(users, file, indent=4, ensure_ascii=False)


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

        if user_exists(login, email, phone):
            QMessageBox.critical(self, "Ошибка", "Пользователь с такими данными уже существует.")
            return

        user_data = {
            'login': login,
            'password': hash_password(password),
            'email': email,
            'phone': phone
        }

        save_user(user_data)
        QMessageBox.information(self, "Успех", "Вы успешно зарегистрированы!")
        self.initUI()

    def performLogin(self):
        login = self.loginUsernameEdit.text()
        password = self.loginPasswordEdit.text()

        try:
            with open('database.json', 'r', encoding='utf-8') as file:
                users = json.load(file)
                for user in users:
                    if user['login'] == login and user['password'] == hash_password(password):
                        QMessageBox.information(self, "Успех", "Авторизация успешна. Добро пожаловать!")
                        return
        except FileNotFoundError:
            QMessageBox.critical(self, "Ошибка", "Файл с данными пользователя не найден.")
            return

        QMessageBox.critical(self, "Ошибка", "Логин или пароль неверны.")
        return


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
