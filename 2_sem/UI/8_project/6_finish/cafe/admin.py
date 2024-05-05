from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QMessageBox, QComboBox, QTextEdit,
                             QDialogButtonBox, QDialog, QTableWidget, QTableWidgetItem, QHeaderView)
from datetime import datetime
import hashlib
from PyQt6.QtCore import Qt
from sqlalchemy.exc import SQLAlchemyError
from string import punctuation, ascii_letters
from info import column_names_users, User, session, RUSSIAN_ALPHABET, Journal, column_names_journal


class AdminStartingWindow(QWidget):
    def __init__(self, current_user):
        super().__init__()
        self.current_user = current_user
        self.setWindowTitle("Административная панель")
        layout = QVBoxLayout()

        self.user_management_button = QPushButton("Управление пользователями")
        self.user_management_button.clicked.connect(self.open_user_management)

        self.journal_button = QPushButton("Журнал событий")
        self.journal_button.clicked.connect(self.open_journal)

        self.btnMenu = QPushButton('Меню', self)
        self.btnMenu.clicked.connect(self.open_confirm_menu)

        layout.addWidget(self.user_management_button)
        layout.addWidget(self.journal_button)
        layout.addWidget(self.btnMenu)
        self.setLayout(layout)

        self.setStyleSheet("""
                    QWidget {
                        font-family: 'Arial';
                        font-size: 14px;
                    }
                    QPushButton {
                        background-color: #5CACEE;
                        color: white;
                        border-style: outset;
                        border-width: 2px;
                        border-radius: 10px;
                        border-color: beige;
                        font: bold 14px;
                        min-width: 20em;
                        padding: 10px;
                        margin: 10px;
                    }
                    QPushButton:hover {
                        background-color: #1E90FF;
                        border-style: inset;
                    }
                """)

    def open_user_management(self):
        self.admin_window = AdminWindow(self.current_user)
        self.admin_window.show()

    def open_journal(self):
        self.journal_window = JournalWindow()
        self.journal_window.show()

    def open_confirm_menu(self):
        msg_box = QMessageBox()
        msg_box.setWindowTitle("Переход в меню")
        msg_box.setText("Точно ли вы хотите перейти на экран меню?")
        msg_box.setStandardButtons(QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        msg_box.setDefaultButton(QMessageBox.StandardButton.No)
        result = msg_box.exec()

        if result == QMessageBox.StandardButton.Yes:
            self.open_menu()

    def open_menu(self):
        from cafe import MainMenuWindow

        self.menu_window = MainMenuWindow(self.current_user)
        self.menu_window.show()
        self.close()


class JournalWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Журнал событий")
        self.setGeometry(100, 100, 800, 600)
        layout = QVBoxLayout()

        self.table = QTableWidget(0, len(column_names_journal))
        self.table.setHorizontalHeaderLabels(column_names_journal)
        self.table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.table.setSelectionMode(QTableWidget.SelectionMode.SingleSelection)
        self.table.verticalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Interactive)

        header = self.table.horizontalHeader()
        for i in range(len(column_names_journal)):
            header.setSectionResizeMode(i, QHeaderView.ResizeMode.Stretch)

        self.load_journal_events()

        self.table.setSortingEnabled(True)
        self.table.sortItems(0, Qt.SortOrder.AscendingOrder)

        layout.addWidget(self.table)
        self.setLayout(layout)

        self.setStyleSheet("""
                    QWidget {
                        font-family: 'Arial';
                        font-size: 14px;
                    }
                    QPushButton {
                        background-color: #5CACEE;
                        color: white;
                        border-style: outset;
                        border-width: 2px;
                        border-radius: 10px;
                        border-color: beige;
                        font: bold 14px;
                        min-width: 10em;
                        padding: 6px;
                    }
                    QPushButton:hover {
                        background-color: #1E90FF;
                        border-style: inset;
                    }
                    QPushButton:pressed {
                        background-color: #4682B4;
                        border-style: inset;
                    }
                    QTableWidget {
                        border: 1px solid #C0C0C0;
                        gridline-color: #C0C0C0;
                        selection-background-color: #B0E2FF;
                    }
                    QHeaderView::section {
                        background-color: #87CEFA;
                        padding: 4px;
                        border: 1px solid #C0C0C0;
                        font-size: 14px;
                    }
                    QComboBox {
                        border: 1px solid #C0C0C0;
                        border-radius: 5px;
                        padding: 1px 18px 1px 3px;
                        min-width: 6em;
                    }
                    QComboBox:editable {
                        background: white;
                    }
                    QComboBox:!editable, QComboBox::drop-down:editable {
                         background: #87CEFA;
                    }
                    QComboBox:!editable:on, QComboBox::drop-down:editable:on {
                        background: #B0E2FF;
                    }
                    """)

    def load_journal_events(self):
        self.table.setRowCount(0)
        events = session.query(Journal).all()
        for event in events:
            row_position = self.table.rowCount()
            self.table.insertRow(row_position)
            for i, field in enumerate(
                    [event.id, event.action, event.time, event.details, event.first_name, event.last_name, event.role]):
                if i == 3:
                    text_edit = QTextEdit(str(field))
                    self.table.setCellWidget(row_position, i, text_edit)
                    self.table.horizontalHeader().setSectionResizeMode(i, QHeaderView.ResizeMode.Stretch)
                else:
                    item = QTableWidgetItem(str(field))
                    self.table.setItem(row_position, i, item)
                    self.table.horizontalHeader().setSectionResizeMode(i, QHeaderView.ResizeMode.ResizeToContents)


class UserInfoDialog(QDialog):
    def __init__(self, action, **kwargs):
        super().__init__()
        self.setWindowTitle("Информация о пользователе")
        layout = QVBoxLayout(self)

        if action == "add":
            details = f'Добавлен новый пользователь:\nЛогин: {kwargs["login"]}\nПароль: {kwargs["password"]}\n' \
                      f'Email: {kwargs["email"]}\nТелефон: {kwargs["phone"]}\nИмя: {kwargs["first_name"]}\n' \
                      f'Фамилия: {kwargs["last_name"]}\nРоль: {kwargs["role"]}'
        elif action == "edit":
            details = f'Изменены данные пользователя:\nЛогин: {kwargs["login"]}\n' \
                      f'Пароль: {kwargs["password"]}\nEmail: {kwargs["email"]}\nТелефон: {kwargs["phone"]}\n' \
                      f'Имя: {kwargs["first_name"]}\nФамилия: {kwargs["last_name"]}\nРоль: {kwargs["role"]}'
        elif action == "delete":
            details = f'Удалены данные пользователя:\nЛогин: {kwargs["login"]}\n' \
                      f'Пароль: {kwargs["password"]}\nEmail: {kwargs["email"]}\nТелефон: {kwargs["phone"]}\n' \
                      f'Имя: {kwargs["first_name"]}\nФамилия: {kwargs["last_name"]}\nРоль: {kwargs["role"]}'

        label = QLabel(details)
        layout.addWidget(label)

        buttons = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel)
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)
        layout.addWidget(buttons)

        self.setLayout(layout)


class AdminWindow(QWidget):
    def __init__(self, current_user):
        super().__init__()
        self.current_user = current_user
        self.setWindowTitle('Управление пользователями')
        self.setGeometry(100, 100, 800, 600)
        self.roles = ['client', 'manager', 'waiter']
        self.initUI()
        self.action = None

    def initUI(self):
        layout = QVBoxLayout()

        self.table = QTableWidget(0, len(column_names_users))
        self.table.setHorizontalHeaderLabels(column_names_users)
        self.table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.table.setSelectionMode(QTableWidget.SelectionMode.SingleSelection)
        self.table.verticalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Interactive)

        header = self.table.horizontalHeader()
        for i in range(len(column_names_users)):
            header.setSectionResizeMode(i, QHeaderView.ResizeMode.Stretch)

        btn_layout = QHBoxLayout()
        self.btnAddUser = QPushButton('Добавить', self)
        self.btnDeleteUser = QPushButton('Удалить', self)
        self.btnSaveChanges = QPushButton('Сохранить изменения')
        self.load_users()

        self.table.setSortingEnabled(True)
        self.table.sortItems(0, Qt.SortOrder.AscendingOrder)

        btn_layout.addWidget(self.btnAddUser)
        btn_layout.addWidget(self.btnDeleteUser)
        btn_layout.addWidget(self.btnSaveChanges)

        self.btnAddUser.clicked.connect(self.add_user)
        self.btnDeleteUser.clicked.connect(self.delete_user)
        self.btnSaveChanges.clicked.connect(self.save_user)

        layout.addWidget(self.table)
        layout.addLayout(btn_layout)
        self.setLayout(layout)

        self.setStyleSheet("""
            QWidget {
                font-family: 'Arial';
                font-size: 14px;
            }
            QPushButton {
                background-color: #5CACEE;
                color: white;
                border-style: outset;
                border-width: 2px;
                border-radius: 10px;
                border-color: beige;
                font: bold 14px;
                min-width: 10em;
                padding: 6px;
            }
            QPushButton:hover {
                background-color: #1E90FF;
                border-style: inset;
            }
            QPushButton:pressed {
                background-color: #4682B4;
                border-style: inset;
            }
            QTableWidget {
                border: 1px solid #C0C0C0;
                gridline-color: #C0C0C0;
                selection-background-color: #B0E2FF;
            }
            QHeaderView::section {
                background-color: #87CEFA;
                padding: 4px;
                border: 1px solid #C0C0C0;
                font-size: 14px;
            }
            QComboBox {
                border: 1px solid #C0C0C0;
                border-radius: 5px;
                padding: 1px 18px 1px 3px;
                min-width: 6em;
            }
            QComboBox:editable {
                background: white;
            }
            QComboBox:!editable, QComboBox::drop-down:editable {
                 background: #87CEFA;
            }
            QComboBox:!editable:on, QComboBox::drop-down:editable:on {
                background: #B0E2FF;
            }
            """)

        self.btnAddUser.setStyleSheet("QPushButton {background-color: #32CD32; color: white;}")
        self.btnDeleteUser.setStyleSheet("QPushButton {background-color: #FF6347; color: white;}")
        self.btnSaveChanges.setStyleSheet("QPushButton {background-color: #5CACEE; color: white;}")

    def load_users(self):
        self.table.setSortingEnabled(False)
        self.table.setRowCount(0)

        users = session.query(User).filter(
            User.role != 'admin').all()
        for user in users:
            row_position = self.table.rowCount()
            self.table.insertRow(row_position)

            id_item = QTableWidgetItem(str(user.id))
            id_item.setFlags(id_item.flags() & ~Qt.ItemFlag.ItemIsEditable)
            self.table.setItem(row_position, 0, id_item)

            fields = [user.login, user.password, user.email, user.phone, user.first_name, user.last_name]
            for i, field in enumerate(fields, start=1):
                item = QTableWidgetItem(str(field))
                item.setFlags(item.flags() | Qt.ItemFlag.ItemIsEditable)
                self.table.setItem(row_position, i, item)

            combo_box = QComboBox()
            combo_box.addItems(self.roles)
            combo_box.setCurrentText(user.role)
            combo_box.setEditable(True)
            self.table.setCellWidget(row_position, 7, combo_box)
            self.table.setSortingEnabled(True)
            self.table.sortItems(0, Qt.SortOrder.AscendingOrder)

    def add_user(self):
        row_position = self.table.rowCount()
        self.table.insertRow(row_position)
        for i in range(1, len(column_names_users) - 1):
            self.table.setItem(row_position, i, QTableWidgetItem(""))
        combo_box = QComboBox()
        combo_box.addItems(self.roles)
        self.table.setCellWidget(row_position, len(column_names_users) - 1, combo_box)
        self.table.editItem(self.table.item(row_position, 1))
        self.action = 'add'

    def save_user(self):
        row_count = self.table.currentRow()
        if row_count != -1:
            login = self.table.item(row_count, 1).text()
            password = self.table.item(row_count, 2).text()
            email = self.table.item(row_count, 3).text()
            phone = self.table.item(row_count, 4).text()
            first_name = self.table.item(row_count, 5).text()
            last_name = self.table.item(row_count, 6).text()
            role_combo = self.table.cellWidget(row_count, 7)
            role = role_combo.currentText()

            if len(login) < 5 or not all(char in ascii_letters + '0123456789' for char in login):
                QMessageBox.critical(self, "Ошибка",
                                     "Логин должен быть не менее 5 символов и содержать только буквы и цифры.")
                return
            if len(password) < 64:
                if len(password) < 8 or not any(char.isdigit() for char in password) or not any(
                        char.isupper() for char in password) \
                        or not any(char.islower() for char in password) or not any(
                    char in punctuation for char in password):
                    QMessageBox.critical(self, "Ошибка",
                                         "Пароль должен быть не менее 8 символов, содержать цифры, заглавные и строчные буквы,"
                                         " а также специальные символы.")
                    return
                new_password = self.hash_password(password)

            if '@' not in email or email.count('@') > 1 or email.startswith('@') or email.endswith('@'):
                QMessageBox.critical(self, "Ошибка", "Некорректный формат email.")
                return
            if not (phone.startswith('+7') or phone.startswith('8')) or len(phone.strip('+')) != 11:
                QMessageBox.critical(self, "Ошибка", "Телефон должен начинаться на +7 или 8 и содержать 11 цифр.")
                return
            if not all(char.isalpha() for char in first_name) or not all(
                    char in RUSSIAN_ALPHABET for char in first_name.lower()):
                QMessageBox.critical(self, "Ошибка", "Имя должно содержать только буквы русского алфавита.")
                return
            if not all(char.isalpha() for char in last_name) or not all(
                    char in RUSSIAN_ALPHABET for char in last_name.lower()):
                QMessageBox.critical(self, "Ошибка", "Фамилия должна содержать только буквы русского алфавита.")
                return
            if len(password) >= 64:
                new_password = password
            if self.action == 'add':
                if self.user_exists(login, email, phone):
                    QMessageBox.critical(self, "Ошибка", "Пользователь с такими данными уже существует.")
                    return
                dialog = UserInfoDialog('add', login=login, password=password, email=email, phone=phone,
                                        first_name=first_name, last_name=last_name, role=role)
                result = dialog.exec()
                if result == QDialog.DialogCode.Accepted:
                    new_user = User(login=login, password=new_password, email=email, phone=phone, first_name=first_name,
                                    last_name=last_name, role=role)
                    session.add(new_user)
                    session.commit()

                    journal = Journal(action='add', time=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                                      details=f'Добавление пользователя с логином: {login}',
                                      first_name=self.current_user.first_name, last_name=self.current_user.last_name,
                                      role=self.current_user.role)
                    session.add(journal)
                    session.commit()
                    QMessageBox.information(self, "Успех", "Пользователь успешно добавлен.")
                self.action = None
            else:
                user_id = int(self.table.item(row_count, 0).text())
                dialog = UserInfoDialog('edit', login=login, password=password, email=email, phone=phone,
                                        first_name=first_name, last_name=last_name, role=role)
                result = dialog.exec()
                if result == QDialog.DialogCode.Accepted:
                    self.update_user(user_id, login, new_password, email, phone, first_name, last_name, role)
                    journal = Journal(action='edit', time=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                                      details=f'Изменение пользователя с ID: {user_id}',
                                      first_name=self.current_user.first_name, last_name=self.current_user.last_name,
                                      role=self.current_user.role)
                    session.add(journal)
                    session.commit()
                    QMessageBox.information(self, "Успех", "Пользователь успешно изменен.")
            self.load_users()
        else:
            QMessageBox.warning(self, "Внимание", "Пожалуйста, выберите пользователя.")
            return

    def update_user(self, user_id, login, password, email, phone, first_name, last_name, role):
        try:
            user = session.query(User).filter(User.id == user_id).first()
            if user:
                user.login = login
                user.password = password
                user.email = email
                user.phone = phone
                user.first_name = first_name
                user.last_name = last_name
                user.role = role
                session.commit()
            else:
                QMessageBox.information(self, 'Ошибка', f'Пользователь с логином: {login} не найден.')
        except SQLAlchemyError as e:
            print("Ошибка при обновлении пользователя:", e)
            session.rollback()
            QMessageBox.information(self, 'Ошибка', f'Ошибка при обновлении пользователя: {e}')
            return

    def delete_user(self):
        current_row = self.table.currentRow()
        if current_row != -1:
            user_id = int(self.table.item(current_row, 0).text())
            user = session.query(User).filter(User.id == user_id).first()
            dialog = UserInfoDialog('delete', login=user.login, password=user.password, email=user.email,
                                    phone=user.phone,
                                    first_name=user.first_name, last_name=user.last_name, role=user.role)
            result = dialog.exec()

            if result == QDialog.DialogCode.Accepted:
                try:
                    session.delete(user)
                    session.commit()

                    self.table.removeRow(current_row)

                    journal = Journal(action='delete', time=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                                      details=f'Удаление пользователя с данными: \nЛогин: {user.login}\n'
                                              f'Пароль: {user.password}\nEmail: {user.email}\nТелефон: {user.phone}\n'
                                              f'Имя: {user.first_name}\nФамилия: {user.last_name}\n'
                                              f'Роль: {user.role}', first_name=self.current_user.first_name,
                                      last_name=self.current_user.last_name, role=self.current_user.role)
                    session.add(journal)
                    session.commit()

                    QMessageBox.information(self, "Успех", "Пользователь успешно удален.")
                except Exception as e:
                    QMessageBox.critical(self, "Ошибка", f"Не удалось удалить пользователя: {e}")
                    session.rollback()
        else:
            QMessageBox.warning(self, "Внимание", "Пожалуйста, выберите пользователя.")

    def hash_password(self, password):
        return hashlib.sha256(password.encode()).hexdigest()

    def user_exists(self, login, email, phone):
        user = session.query(User).filter(
            (User.login == login) | (User.email == email) | (User.phone == phone)).first()
        return user is not None

    def sort_table(self, column):
        self.table.sortItems(column)
