import sys
from string import punctuation, ascii_letters
from PyQt6.QtWidgets import (QApplication, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QLineEdit,
                             QMessageBox, QGridLayout, QSizePolicy, QComboBox, QScrollArea, QDateEdit,
                             QTextEdit, QSpinBox, QTimeEdit, QDialogButtonBox, QDialog, QCheckBox)
import hashlib
import time
import json

from datetime import datetime, timedelta
from PyQt6.QtGui import QIcon, QPixmap
from PyQt6.QtCore import Qt, QDate, QTime

from info import session, RUSSIAN_ALPHABET, START_TIME, END_TIME, Reservation, DELTA_HOUR, MAX_TABLES, Session, \
    MenuItem, or_, User
from admin import AdminStartingWindow
from manager import ManagerStartingWindow
from waiter import WaiterStartingWindow


def save_auth_data(login, remember_me):
    if remember_me:
        auth_data = {
            'login': login,
            'timestamp': time.time()
        }
        with open('auth_data.json', 'w') as f:
            json.dump(auth_data, f)


def is_auth_valid():
    try:
        with open('auth_data.json', 'r') as f:
            auth_data = json.load(f)
        remember_me_timedelta = time.time() - auth_data['timestamp'] < 18000
        if not remember_me_timedelta:
            with open('auth_data.json', 'w') as f:
                f.write('')
        return remember_me_timedelta
    except (FileNotFoundError, json.JSONDecodeError):
        return False


def get_current_user():
    try:
        with open('auth_data.json', 'r') as f:
            auth_data = json.load(f)
        login = auth_data['login']
        user = session.query(User).filter_by(login=login).first()
    except (FileNotFoundError, json.JSONDecodeError):
        return None
    return user


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


class Registration(QWidget):
    def __init__(self, parent_window):
        super().__init__()
        self.setWindowTitle("Регистрация")
        self.setGeometry(100, 100, 300, 400)
        self.parent_window = parent_window
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)
        self.initUI()
        self.setStyleSheet("""
                    QWidget {
                        font-family: 'Segoe UI', Arial, sans-serif;
                        font-size: 14px;
                        background-color: #FFF;
                        color: #333;
                    }
                    QLabel {
                        margin-bottom: 5px;
                    }
                    QLineEdit {
                        padding: 10px;
                        border: 1px solid #ccc;
                        border-radius: 5px;
                        margin-bottom: 10px;
                    }
                    QPushButton {
                        background-color: #007bff;
                        color: white;
                        border: none;
                        padding: 10px 15px;
                        border-radius: 5px;
                        margin-top: 10px;
                        font-weight: bold;
                    }
                    QPushButton:pressed {
                        background-color: #0056b3;
                    }
                    QListWidget {
                        border: none;
                    }
                    QListWidgetItem {
                        border-bottom: 1px solid #eee;
                        padding: 10px;
                    }
                """)

    def initUI(self):
        self.clearLayout(self.layout)

        centerWidget = QWidget()
        centerLayout = QVBoxLayout()
        centerWidget.setLayout(centerLayout)

        self.registrationForm()

    def clearLayout(self, layout):
        while layout.count():
            child = layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()
            elif child.layout():
                self.clearLayout(child)

    def registration(self):
        self.clearLayout(self.layout)
        self.registrationForm()

    def registrationForm(self):

        self.first_lastname = QHBoxLayout()
        self.firstname = QVBoxLayout()
        self.lastname = QVBoxLayout()

        self.firstNameLabel = QLabel("Имя:")
        self.firstNameEdit = QLineEdit()
        self.firstname.addWidget(self.firstNameLabel)
        self.firstname.addWidget(self.firstNameEdit)

        self.lastNameLabel = QLabel("Фамилия:")
        self.lastNameEdit = QLineEdit()
        self.lastname.addWidget(self.lastNameLabel)
        self.lastname.addWidget(self.lastNameEdit)

        self.first_lastname.addLayout(self.firstname)
        self.first_lastname.addLayout(self.lastname)

        self.usernameLabel = QLabel("Логин:")
        self.usernameEdit = QLineEdit()
        self.passwordLabel = QLabel("Пароль:")
        self.passwordEdit = PasswordLineEdit("icons/eye_slash_icon.png", "icons/eye_icon.png")
        self.layout.addWidget(self.passwordEdit)

        self.emailLabel = QLabel("Email:")
        self.emailEdit = QLineEdit()
        self.phoneLabel = QLabel("Телефон:")
        self.phoneEdit = QLineEdit()
        self.remember_me_checkbox = QCheckBox("Запомни меня", self)
        self.registerButton = QPushButton("Зарегистрироваться")

        self.layout.addLayout(self.first_lastname)
        self.layout.addWidget(self.usernameLabel)
        self.layout.addWidget(self.usernameEdit)
        self.layout.addWidget(self.passwordLabel)
        self.layout.addWidget(self.passwordEdit)
        self.layout.addWidget(self.emailLabel)
        self.layout.addWidget(self.emailEdit)
        self.layout.addWidget(self.phoneLabel)
        self.layout.addWidget(self.phoneEdit)
        self.layout.addWidget(self.remember_me_checkbox)
        self.layout.addWidget(self.registerButton)

        self.registerButton.clicked.connect(self.performRegistration)

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
        remember_me = self.remember_me_checkbox.isChecked()
        first_name = self.firstNameEdit.text()
        last_name = self.lastNameEdit.text()

        if not all(char.isalpha() for char in first_name) or not all(
                char in RUSSIAN_ALPHABET for char in first_name.lower()):
            QMessageBox.critical(self, "Ошибка", "Имя должно содержать только буквы русского алфавита.")
            return
        if not all(char.isalpha() for char in last_name) or not all(
                char in RUSSIAN_ALPHABET for char in last_name.lower()):
            QMessageBox.critical(self, "Ошибка", "Фамилия должна содержать только буквы русского алфавита.")
            return
        if len(login) < 5 or not all(char in ascii_letters + '0123456789' for char in login):
            QMessageBox.critical(self, "Ошибка",
                                 "Логин должен быть не менее 5 символов и содержать только буквы и цифры.")
            return
        if len(password) < 8 or not any(char.isdigit() for char in password) or not any(
                char.isupper() for char in password) \
                or not any(char.islower() for char in password) or not any(
            char in punctuation for char in password):
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

        user = self.save_user(login, password, email, phone, first_name, last_name)
        save_auth_data(user.login, remember_me)
        QMessageBox.information(self, "Успех", "Вы успешно зарегистрированы!")
        self.current_user = user
        self.menu_window = MainMenuWindow(user)
        self.hide()
        self.parent_window.close()
        self.menu_window.show()

    def save_user(self, login, password, email, phone, first_name, last_name):
        hashed_password = self.hash_password(password)
        new_user = User(login=login, password=hashed_password, email=email, phone=phone,
                        first_name=first_name, last_name=last_name)
        session.add(new_user)
        session.commit()
        return new_user

    def hash_password(self, password):
        return hashlib.sha256(password.encode()).hexdigest()

    def user_exists(self, login, email, phone):
        user = session.query(User).filter(
            (User.login == login) | (User.email == email) | (User.phone == phone)).first()
        return user is not None


class Authorization(QWidget):
    def __init__(self, parent_window):
        super().__init__()
        self.setWindowTitle("Вход")
        self.setGeometry(100, 100, 300, 400)
        self.parent_window = parent_window
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)
        self.initUI()
        self.setStyleSheet("""
                    QWidget {
                        font-family: 'Segoe UI', Arial, sans-serif;
                        font-size: 14px;
                        background-color: #FFF;
                        color: #333;
                    }
                    QLabel {
                        margin-bottom: 5px;
                    }
                    QLineEdit {
                        padding: 10px;
                        border: 1px solid #ccc;
                        border-radius: 5px;
                        margin-bottom: 10px;
                    }
                    QPushButton {
                        background-color: #007bff;
                        color: white;
                        border: none;
                        padding: 10px 15px;
                        border-radius: 5px;
                        margin-top: 10px;
                        font-weight: bold;
                    }
                    QPushButton:pressed {
                        background-color: #0056b3;
                    }
                    QListWidget {
                        border: none;
                    }
                    QListWidgetItem {
                        border-bottom: 1px solid #eee;
                        padding: 10px;
                    }
                """)

    def initUI(self):
        self.clearLayout(self.layout)

        centerWidget = QWidget()
        centerLayout = QVBoxLayout()
        centerWidget.setLayout(centerLayout)

        self.loginForm()

    def clearLayout(self, layout):
        while layout.count():
            child = layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()
            elif child.layout():
                self.clearLayout(child)

    def login(self):
        self.clearLayout(self.layout)
        self.loginForm()

    def loginForm(self):
        self.loginUsernameLabel = QLabel("Логин:")
        self.loginUsernameEdit = QLineEdit()
        self.loginPasswordLabel = QLabel("Пароль:")
        self.loginPasswordEdit = QLineEdit()
        self.loginPasswordEdit = PasswordLineEdit("icons/eye_slash_icon.png", "icons/eye_icon.png")
        self.remember_me_checkbox = QCheckBox("Запомни меня", self)
        self.loginButton = QPushButton("Войти")

        self.layout.addWidget(self.loginUsernameLabel)
        self.layout.addWidget(self.loginUsernameEdit)
        self.layout.addWidget(self.loginPasswordLabel)
        self.layout.addWidget(self.loginPasswordEdit)
        self.layout.addWidget(self.remember_me_checkbox)
        self.layout.addWidget(self.loginButton)

        self.loginButton.clicked.connect(self.performLogin)

    def togglePasswordVisibility(self, passwordEdit):
        if passwordEdit.echoMode() == QLineEdit.EchoMode.Password:
            passwordEdit.setEchoMode(QLineEdit.EchoMode.Normal)
        else:
            passwordEdit.setEchoMode(QLineEdit.EchoMode.Password)

    def performLogin(self):
        login = self.loginUsernameEdit.text()
        password = self.loginPasswordEdit.text()
        remember_me = self.remember_me_checkbox.isChecked()
        if self.validate_credentials(login, password):
            save_auth_data(login, remember_me)
            QMessageBox.information(self, "Успех", "Авторизация успешна. Добро пожаловать!")
            self.hide()
            self.parent_window.close()
            user = session.query(User).filter_by(login=login).first()
            self.current_user = user
            if user.role == 'admin':
                self.admin_window = AdminStartingWindow(self.current_user)
                self.admin_window.show()
            elif user.role == 'manager':
                self.manager_window = ManagerStartingWindow(self.current_user)
                self.manager_window.show()
            elif user.role == 'waiter':
                self.waiter_window = WaiterStartingWindow(self.current_user)
                self.waiter_window.show()
            elif user.role == 'client':
                self.menu_window = MainMenuWindow(self.current_user)
                self.menu_window.show()
        else:
            QMessageBox.critical(self, "Ошибка", "Логин или пароль неверны.")

    def validate_credentials(self, login, password):
        user = session.query(User).filter_by(login=login).first()
        if user and user.password == self.hash_password(password):
            return True
        return False

    def save_user(self, login, password, email, phone, first_name, last_name):
        hashed_password = self.hash_password(password)
        new_user = User(login=login, password=hashed_password, email=email, phone=phone,
                        first_name=first_name, last_name=last_name)
        session.add(new_user)
        session.commit()

    def hash_password(self, password):
        return hashlib.sha256(password.encode()).hexdigest()

    def user_exists(self, login, email, phone):
        user = session.query(User).filter((User.login == login) | (User.email == email) | (User.phone == phone)).first()
        return user is not None


class ConfirmReservationDialog(QDialog):
    def __init__(self, reservation_details, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Подтверждение бронирования")
        self.setGeometry(500, 300, 350, 200)
        layout = QVBoxLayout()

        details = f"""
        Бронь на имя: {reservation_details['first_name']}
        Телефон: {reservation_details['phone']}
        Дата: {reservation_details['date']}
        Время: {reservation_details['time']}
        Количество гостей: {reservation_details['guest_count']}
        Тип столика: {reservation_details['table_type']}
        Особые пожелания: {reservation_details['special_requests']}
        """
        layout.addWidget(QLabel(details))

        buttons = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel)
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)
        layout.addWidget(buttons)

        self.setLayout(layout)


class ReservationWindow(QWidget):
    def __init__(self, current_user, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Бронирование столика")
        self.setWindowFlags(Qt.WindowType.Window)
        self.setGeometry(400, 200, 300, 400)

        self.current_user = current_user

        self.show()
        layout = QVBoxLayout()
        if current_user is None:
            self.first_name_edit = QLineEdit()
            self.last_name_edit = QLineEdit()
            self.phone = QLineEdit()
            layout.addWidget(QLabel("Имя:"))
            layout.addWidget(self.first_name_edit)
            layout.addWidget(QLabel('Телефон:'))
            layout.addWidget(self.phone)

        self.date_edit = QDateEdit(QDate.currentDate())
        self.date_edit.setCalendarPopup(True)
        self.date_edit.setDisplayFormat("yyyy-MM-dd")
        layout.addWidget(QLabel("Дата:"))
        layout.addWidget(self.date_edit)

        self.time_edit = QTimeEdit(QTime.currentTime())
        self.time_edit.setDisplayFormat("HH:mm")
        self.time_edit.setMinimumTime(QTime(START_TIME[0], START_TIME[1]))
        self.time_edit.setMaximumTime(QTime(END_TIME[0], END_TIME[1]))
        layout.addWidget(QLabel("Время:"))
        layout.addWidget(self.time_edit)

        self.guest_count_spin = QSpinBox()
        self.guest_count_spin.setMinimum(1)
        self.guest_count_spin.setMaximum(20)
        layout.addWidget(QLabel("Количество гостей:"))
        layout.addWidget(self.guest_count_spin)

        self.table_type_combo = QComboBox()
        self.table_type_combo.addItems(["Обычный", "VIP", "На террасе"])
        layout.addWidget(QLabel("Тип столика:"))
        layout.addWidget(self.table_type_combo)

        self.special_requests_edit = QTextEdit()
        layout.addWidget(QLabel("Особые пожелания:"))
        layout.addWidget(self.special_requests_edit)

        self.reserve_button = QPushButton("Забронировать")
        self.reserve_button.clicked.connect(self.reserve_table)
        layout.addWidget(self.reserve_button)

        self.setLayout(layout)

    def reserve_table(self):
        if self.current_user is None:
            first_name = self.first_name_edit.text()
            if not first_name or not all(char.isalpha() for char in first_name) or not all(
                    char in RUSSIAN_ALPHABET for char in first_name.lower()):
                QMessageBox.critical(self, "Ошибка", "Имя должно содержать только буквы русского алфавита.")
                return
            phone = self.phone.text()
            if not (phone.startswith('+7') or phone.startswith('8')) or len(phone.strip('+')) != 11 or not phone.strip('+').isdigit():
                QMessageBox.critical(self, "Ошибка", "Телефон должен начинаться на +7 или 8 и содержать 11 цифр.")
                return
        else:
            first_name = self.current_user.first_name
            phone = self.current_user.phone
        date = self.date_edit.dateTime().toString("yyyy-MM-dd")
        time = self.time_edit.time().toString("HH:mm")
        guest_count = self.guest_count_spin.value()
        table_type = self.table_type_combo.currentText()
        if not self.is_table_available(date, time, table_type):
            QMessageBox.warning(self, "Ошибка", f"На это время все столики {table_type} уже забронированы.")
            return
        special_requests = self.special_requests_edit.toPlainText()

        reservation = {
            "first_name": first_name,
            "phone": phone,
            "date": date,
            "time": time,
            "guest_count": guest_count,
            "table_type": table_type,
            "special_requests": special_requests
        }
        confirm_dialog = ConfirmReservationDialog(reservation, self)
        result = confirm_dialog.exec()
        if result == QDialog.DialogCode.Accepted:
            reservation = Reservation(
                date=date,
                time=time,
                guest_count=guest_count,
                table_type=table_type,
                special_requests=special_requests,
                first_name=first_name,
                phone=phone
            )
            session.add(reservation)
            session.commit()
            QMessageBox.information(self, "Бронирование подтверждено", "Ваш столик успешно забронирован!")
            self.hide()
        else:
            QMessageBox.warning(self, "Бронирование отменено", "Бронирование было отменено.")

    def is_table_available(self, date, time, table_type):
        requested_datetime = datetime.strptime(f"{date} {time}", "%Y-%m-%d %H:%M")
        lower_bound = (requested_datetime - timedelta(hours=DELTA_HOUR))
        upper_bound = (requested_datetime + timedelta(hours=DELTA_HOUR))

        reservations = session.query(Reservation).filter(
            Reservation.date == date,
            Reservation.table_type == table_type,
        ).all()

        reservations_count = sum(
            lower_bound <= datetime.strptime(f"{elem.date} {elem.time}", "%Y-%m-%d %H:%M") <= upper_bound for elem in
            list(reservations))

        return reservations_count < MAX_TABLES[table_type]


class MenuItemWidget(QWidget):
    def __init__(self, item_data, parent=None):
        super().__init__(parent)
        self.layout = QVBoxLayout()

        self.setSizePolicy(
            QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding))

        self.image_label = QLabel(self)
        pixmap = QPixmap(item_data['image'])
        pixmap = pixmap.scaled(200, 400, Qt.AspectRatioMode.KeepAspectRatio)
        self.image_label.setPixmap(pixmap)
        self.image_label.setAlignment(Qt.AlignmentFlag.AlignLeft)

        self.image_label.setStyleSheet('margin-bottom:20px;')

        self.card = QVBoxLayout()

        self.name_label = QLabel(item_data['name'])
        self.description_label = QLabel(item_data['description'])
        self.price_label = QLabel(item_data['price'])
        self.description_label.setWordWrap(True)
        self.card.addWidget(self.name_label)
        self.card.addWidget(self.description_label)

        self.name_label.setAlignment(Qt.AlignmentFlag.AlignBottom)
        self.description_label.setAlignment(Qt.AlignmentFlag.AlignBottom)
        self.price_label.setAlignment(Qt.AlignmentFlag.AlignBottom)

        self.layout.addWidget(self.image_label)
        self.layout.addLayout(self.card)
        self.layout.addWidget(self.price_label)
        self.setLayout(self.layout)

        self.setStyleSheet("""
            QLabel {
                font-size: 16px;
                color: #333;
            }
            QLabel#nameLabel {
                font-weight: bold;
            }
            QLabel#priceLabel {
                font-size: 14px;
                color: green;
                font-weight: bold;
            }
        """)
        self.name_label.setObjectName("nameLabel")
        self.price_label.setObjectName("priceLabel")


class MainMenuWindow(QWidget):
    def __init__(self, current_user, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Меню")
        self.setGeometry(300, 300, 600, 400)
        self.setMinimumSize(800, 600)

        self.current_user = current_user

        self.scrollArea = QScrollArea(self)
        self.scrollArea.setWidgetResizable(True)
        self.scrollAreaWidgetContents = QWidget()
        self.scrollArea.setWidget(self.scrollAreaWidgetContents)

        self.scrollArea.setStyleSheet("border: none;")

        self.layout = QVBoxLayout(self.scrollAreaWidgetContents)

        self.setupUI()

    def setupUI(self):
        header_layout = QHBoxLayout()
        header_label = QLabel()
        header_text = """
        <style>
            a { text-decoration: none; color: #3498db; font-weight: bold; font-size: 14px; }
            a:hover { text-decoration: underline; color: #2980b9; }
        </style>
        <a href='register'>Регистрация</a> | <a href='login'>Авторизация</a>
        """
        header_label.setText(header_text)
        header_label.setOpenExternalLinks(False)
        header_label.linkActivated.connect(self.handle_link_activation)
        header_label.setAlignment(Qt.AlignmentFlag.AlignRight)
        header_layout.addWidget(header_label)

        self.search_filter = QHBoxLayout()

        self.search_field = QLineEdit(self)
        self.search_button = QPushButton(QIcon("icons/search.png"), "", self)
        self.search_field.setStyleSheet('padding: 5px; border-radius: 5px; border: 2px solid #ccc; font-size: 14px;')
        self.search_button.clicked.connect(self.filter_menu_items)
        self.search_button.setStyleSheet("background: transparent; border: none;")

        self.type_filter = QComboBox(self)
        menu_types = self.get_unique_menu_types()
        menu_types.insert(0, "Все")
        self.type_filter.addItems(menu_types)
        self.type_filter.currentTextChanged.connect(self.filter_by_type)

        self.sort_asc_button = QPushButton(QIcon("icons/arrow_up.png"), "", self)
        self.sort_asc_button.clicked.connect(lambda: self.sort_items(ascending=True))
        self.sort_asc_button.setStyleSheet("background: transparent; border: none;")

        self.sort_desc_button = QPushButton(QIcon("icons/arrow_down.png"), "", self)
        self.sort_desc_button.clicked.connect(lambda: self.sort_items(ascending=False))
        self.sort_desc_button.setStyleSheet("background: transparent; border: none;")

        self.search_filter.addWidget(self.search_field)
        self.search_filter.addWidget(self.search_button)
        self.search_filter.addWidget(self.type_filter)
        self.search_filter.addWidget(self.sort_asc_button)
        self.search_filter.addWidget(self.sort_desc_button)

        self.reserve_table_button = QPushButton("Забронировать столик")
        self.reserve_table_button.clicked.connect(self.reserve_table)
        self.reserve_table_button.setStyleSheet("...")

        self.layout.addLayout(header_layout)
        self.layout.addLayout(self.search_filter)
        self.layout.addStretch(1)
        self.menu_layout = QGridLayout()
        self.load_menu_items()
        self.layout.addLayout(self.menu_layout)
        self.layout.addStretch(1)
        self.layout.addWidget(self.reserve_table_button)

        self.setCentralLayout()
        self.setStyleSheet("""
            QPushButton {
                background-color: #3498db;
                color: white;
                border-radius: 10px;
                padding: 10px 20px;
                font-size: 14px;
                font-weight: bold;
                margin: 5px;
            }
            QPushButton:hover {
                background-color: #2980b9;
            }
            QPushButton:pressed {
                background-color: #2471a3;
            }
            QComboBox {
                padding: 5px;
                border: 2px solid #3498db;
                border-radius: 5px;
                background: white;
                selection-background-color: #3498db;
                color: #333;
                min-width: 150px;
            }

            QComboBox::drop-down {
                subcontrol-origin: padding;
                subcontrol-position: top right;
                width: 25px;
                border-left-width: 1px;
                border-left-color: darkgray;
                border-left-style: solid;
                border-top-right-radius: 3px;
                border-bottom-right-radius: 3px;
            }

            QComboBox::down-arrow {
                width: 16px;
                height: 16px;
                image: url('icons/down_arrow.png');
            }

            QComboBox:hover {
                border: 2px solid #2980b9;
            }

            QScrollArea {
                border: none;
                background-color: #f0f0f0;
            }
            QScrollBar:vertical {
                border: none;
                background: #fff;
                width: 10px;
                margin: 10px 0 10px 0;
            }
            QScrollBar::handle:vertical {
                background: #3498db;
                min-height: 20px;
            }
            QScrollBar::add-line:vertical {
                background: none;
            }
            QScrollBar::sub-line:vertical {
                background: none;
            }
            QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {
                background: none;
            }
        """)

    def get_unique_menu_types(self):
        session = Session()
        types = session.query(MenuItem.type).distinct().all()
        session.close()
        return [t[0].capitalize() for t in types]

    def handle_link_activation(self, link):
        if link == 'register':
            self.registration_form = Registration(self)
            self.registration_form.show()
        elif link == 'login':
            self.authorization_form = Authorization(self)
            self.authorization_form.show()

    def setCentralLayout(self):
        mainLayout = QVBoxLayout(self)
        mainLayout.addWidget(self.scrollArea)
        self.setLayout(mainLayout)

    def sort_items(self, ascending=True):
        search_term = self.search_field.text().lower()
        filter_type = self.type_filter.currentText().lower()
        direction = "asc" if ascending else "desc"
        self.load_menu_items(search_term, filter_type, direction)

    def filter_by_type(self, filter_type):
        filter_type = filter_type.lower()
        if filter_type == "все":
            filter_type = None
        self.load_menu_items(self.search_field.text(), filter_type)

    def clear_layout(self, layout):
        while layout.count():
            child = layout.takeAt(0)
            if child.widget():
                child.widget().setParent(None)

    def filter_menu_items(self):
        search_term = self.search_field.text().lower()
        self.clear_layout(self.menu_layout)
        self.load_menu_items(search_term)

    def load_menu_items(self, search_term='', filter_type=None, sort_direction='asc'):
        self.clear_layout(self.menu_layout)
        menu_items = session.query(MenuItem)

        search_term = search_term.lower()

        if filter_type and filter_type.lower() != 'все':
            menu_items = menu_items.filter(MenuItem.type.ilike(f"%{filter_type}%"))

        if search_term:
            menu_items = session.query(MenuItem).filter(
                or_(
                    MenuItem.name.ilike(f"%{search_term}%"),
                    MenuItem.description.ilike(f"%{search_term}%"),
                    MenuItem.type.ilike(f"%{search_term}%")
                )
            )
            if not menu_items:
                self.no_results(search_term)
                return

        if sort_direction == 'asc':
            menu_items = menu_items.order_by(MenuItem.price.asc())
        else:
            menu_items = menu_items.order_by(MenuItem.price.desc())

        menu_items = menu_items.all()

        if not menu_items:
            no_menu_label = QLabel("Извините, но пока меню не готово")
            no_menu_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            no_menu_label.setStyleSheet("""
                        QLabel {
                            font-size: 24px;
                            font-weight: bold;
                            color: #555;
                            margin-top: 20px;
                            margin-bottom: 20px;
                        }
                    """)
            self.menu_layout.addWidget(no_menu_label, 0, 0)
            return

        row, col = 0, 0
        for item in menu_items:
            menu_item_widget = MenuItemWidget({
                'name': item.name,
                'description': item.description,
                'price': f"{item.price} руб.",
                'image': f'image/{item.photo_path}'
            })
            self.menu_layout.addWidget(menu_item_widget, row, col)
            col += 1
            if col >= 3:
                row += 1
                col = 0

        self.menu_layout.update()
        self.adjustSize()

    def reserve_table(self):
        self.reservation_window = ReservationWindow(self.current_user, self)
        self.reservation_window.show()

    def no_results(self, search_term):
        no_find = QLabel(f'Извините, но мы ничего не нашли по запросу: "{search_term}"')
        no_find.setAlignment(Qt.AlignmentFlag.AlignCenter)
        no_find.setStyleSheet("""
                                                QLabel {
                                                    font-size: 24px;
                                                    font-weight: bold;
                                                    color: #555;
                                                    margin-top: 20px;
                                                    margin-bottom: 20px;
                                                }
                                            """)
        self.menu_layout.addWidget(no_find, 0, 0)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    is_auth = is_auth_valid()
    user = get_current_user()
    if is_auth:
        if user.role == 'admin':
            admin_window = AdminStartingWindow(user)
            admin_window.show()
        elif user.role == 'manager':
            manager_window = ManagerStartingWindow(user)
            manager_window.show()
        elif user.role == 'waiter':
            waiter_window = WaiterStartingWindow(user)
            waiter_window.show()
        elif user.role == 'client':
            main_menu = MainMenuWindow(user)
            main_menu.show()
    else:
        main_menu = MainMenuWindow(user)
        main_menu.show()

    sys.exit(app.exec())
