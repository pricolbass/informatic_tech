import sys
from string import punctuation, ascii_letters
from PyQt6.QtWidgets import (QApplication, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QLineEdit,
                             QMessageBox, QCheckBox, QGridLayout, QSizePolicy, QComboBox, QScrollArea, QDateEdit,
                             QTextEdit, QSpinBox, QTimeEdit)
import hashlib
import json
import time
from PyQt6.QtGui import QFont, QIcon, QPixmap
from PyQt6.QtCore import Qt, QDate, QTime

from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy import or_

Base = declarative_base()


class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    login = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    phone = Column(String, unique=True, nullable=False)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)


class MenuItem(Base):
    __tablename__ = 'menu'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    description = Column(String)
    photo_path = Column(String)
    price = Column(Integer, nullable=False)
    type = Column(String, nullable=False)

    def __repr__(self):
        return f"<MenuItem(type='{self.type}', name='{self.name}', description='{self.description}', price={self.price})>"


class Reservation(Base):
    __tablename__ = 'reservations'
    id = Column(Integer, primary_key=True)
    date = Column(String, nullable=False)
    time = Column(String, nullable=False)
    guest_count = Column(Integer, nullable=False)
    table_type = Column(String, nullable=False)
    special_requests = Column(String)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)

    def __repr__(self):
        return f"<Reservation(date='{self.date}', time='{self.time}', guest_count={self.guest_count}, table_type='{self.table_type}', special_requests='{self.special_requests}')>"


engine = create_engine('sqlite:///database.db', echo=True)
Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()


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
        return time.time() - auth_data['timestamp'] < 18000
    except (FileNotFoundError, json.JSONDecodeError):
        return False


def get_current_user():
    with open('auth_data.json', 'r') as f:
        auth_data = json.load(f)
    login = auth_data['login']
    user = session.query(User).filter_by(login=login).first()
    return user


class ReservationWindow(QWidget):
    def __init__(self, current_user, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Бронирование столика")
        self.setWindowFlags(Qt.WindowType.Window)
        self.setGeometry(400, 200, 300, 400)

        self.current_user = current_user

        self.show()
        layout = QVBoxLayout()

        self.date_edit = QDateEdit(QDate.currentDate())
        self.date_edit.setCalendarPopup(True)
        self.date_edit.setDisplayFormat("yyyy-MM-dd")
        layout.addWidget(QLabel("Дата:"))
        layout.addWidget(self.date_edit)

        self.time_edit = QTimeEdit(QTime.currentTime())
        self.time_edit.setDisplayFormat("HH:mm")
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
        date = self.date_edit.dateTime().toString("yyyy-MM-dd")
        time = self.time_edit.time().toString("HH:mm")
        table_type = self.table_type_combo.currentText()

        existing_reservations = session.query(Reservation).filter_by(date=date, time=time, table_type=table_type).all()
        max_tables = {
            "Обычный": 15,
            "VIP": 5,
            "На террасе": 10
        }
        if len(existing_reservations) >= max_tables[table_type]:
            QMessageBox.warning(self, "Ошибка", f"На это время все столики типа '{table_type}' заняты.")
            return

        reservation = Reservation(
            date=date,
            time=time,
            guest_count=self.guest_count_spin.value(),
            table_type=table_type,
            special_requests=self.special_requests_edit.toPlainText(),
            first_name=self.current_user.first_name,
            last_name=self.current_user.last_name
        )
        session.add(reservation)
        session.commit()
        QMessageBox.information(self, "Успех", "Столик успешно забронирован!")
        self.hide()


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
        self.search_filter = QHBoxLayout()

        self.search_field = QLineEdit(self)
        self.search_button = QPushButton(QIcon("icons/search.png"), "", self)
        self.search_field.setStyleSheet('padding: 5px; border-radius: 5px; border: 2px solid #ccc; font-size: 14px;')
        self.search_button.clicked.connect(self.filter_menu_items)
        self.search_button.setStyleSheet("background: transparent; border: none;")

        self.type_filter = QComboBox(self)
        self.type_filter.addItems(["Все", "Салаты", "Супы", "Основные блюда", 'Пицца', "Напитки"])
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

        self.welcomeLabel = QLabel("Добро пожаловать в приложение кафе с летней террасой!\nВыберите действие:")
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
            elif child.layout():
                self.clearLayout(child)

    def registration(self):
        self.clearLayout(self.layout)
        self.registrationForm()

    def login(self):
        self.clearLayout(self.layout)
        self.loginForm()

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
        self.registerButton = QPushButton("Зарегистрироваться")
        self.backButton = QPushButton("Назад")

        self.layout.addLayout(self.first_lastname)
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
        self.loginPasswordEdit = PasswordLineEdit("icons/eye_slash_icon.png", "icons/eye_icon.png")
        self.remember_me_checkbox = QCheckBox("Запомни меня", self)
        self.loginButton = QPushButton("Войти")
        self.backButton = QPushButton("Назад")

        self.layout.addWidget(self.loginUsernameLabel)
        self.layout.addWidget(self.loginUsernameEdit)
        self.layout.addWidget(self.loginPasswordLabel)
        self.layout.addWidget(self.loginPasswordEdit)
        self.layout.addWidget(self.remember_me_checkbox)
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
        first_name = self.firstNameEdit.text()
        last_name = self.lastNameEdit.text()

        if not all(char.isalpha() for char in first_name):
            QMessageBox.critical(self, "Ошибка", "Имя должно содержать только буквы.")
            return

        if not all(char.isalpha() for char in last_name):
            QMessageBox.critical(self, "Ошибка", "Фамилия должна содержать только буквы.")
            return

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

        self.save_user(login, password, email, phone, first_name, last_name)
        QMessageBox.information(self, "Успех", "Вы успешно зарегистрированы!")
        self.initUI()

    def performLogin(self):
        login = self.loginUsernameEdit.text()
        password = self.loginPasswordEdit.text()
        remember_me = self.remember_me_checkbox.isChecked()
        if self.validate_credentials(login, password):
            save_auth_data(login, remember_me)
            QMessageBox.information(self, "Успех", "Авторизация успешна. Добро пожаловать!")
            self.hide()
            user = session.query(User).filter_by(login=login).first()
            self.current_user = user
            self.menu_window = MainMenuWindow(user)
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


if __name__ == '__main__':
    app = QApplication(sys.argv)
    if is_auth_valid():
        main_menu = MainMenuWindow(get_current_user())
        main_menu.show()
    else:
        main_window = MainWindow()
        main_window.show()
    sys.exit(app.exec())
