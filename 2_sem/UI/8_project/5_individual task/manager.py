from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QMessageBox, QComboBox, QDateEdit,
                             QTextEdit, QTimeEdit, QDialogButtonBox, QDialog, QTableWidget, QTableWidgetItem,
                             QHeaderView)
from datetime import datetime, timedelta
import hashlib
import os
from PyQt6.QtCore import Qt, QDate, QTime
from sqlalchemy.exc import SQLAlchemyError
from string import punctuation, ascii_letters
from info import Reservation, START_TIME, END_TIME, column_names_reservation, column_names_users, User, session, \
    RUSSIAN_ALPHABET, Journal, MenuItem, column_names_menu, DELTA_HOUR, MAX_TABLES
from admin import UserInfoDialog


class ManagerStartingWindow(QWidget):
    def __init__(self, current_user):
        super().__init__()
        self.current_user = current_user
        self.setWindowTitle("Менеджерская панель")
        layout = QVBoxLayout()

        self.menu_management_button = QPushButton("Управление меню")
        self.menu_management_button.clicked.connect(self.open_menu_management)

        self.reservation_management_button = QPushButton("Управление бронью столиков")
        self.reservation_management_button.clicked.connect(self.open_reservation_management)

        self.staff_management_button = QPushButton("Управление персоналом")
        self.staff_management_button.clicked.connect(self.open_staff_management)

        self.btnMenu = QPushButton('Меню', self)
        self.btnMenu.clicked.connect(self.open_confirm_menu)

        layout.addWidget(self.menu_management_button)
        layout.addWidget(self.staff_management_button)
        layout.addWidget(self.reservation_management_button)
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

    def open_menu_management(self):
        self.admin_window = ManagerMenuWindow(self.current_user)
        self.admin_window.show()

    def open_staff_management(self):
        self.manage_staff_window = ManagerStaffWindow(self.current_user)
        self.manage_staff_window.show()

    def open_reservation_management(self):
        self.reservation_management_window = ManagerReservationWindow(self.current_user)
        self.reservation_management_window.show()

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


class ReservationInfoDialog(QDialog):
    def __init__(self, action, **kwargs):
        super().__init__()
        self.setWindowTitle("Информация о блюде")
        layout = QVBoxLayout(self)

        if action == "add":
            details = f'Добавлена новоя бронь:\nДата: {kwargs["date"]}\nВремя: {kwargs["time"]}\n' \
                      f'Количество гостей: {kwargs["guest_count"]}\nТип столика: {kwargs["table_type"]}\n' \
                      f'Особые пожелания: {kwargs["special_requests"]}\nИмя: {kwargs["first_name"]}\nТелефон: {kwargs["phone"]}'
            label = QLabel(details)
            layout.addWidget(label)
        elif action == "edit":
            details = f'Изменены данные блюда:\nДата: {kwargs["date"]}\nВремя: {kwargs["time"]}\n' \
                      f'Количество гостей: {kwargs["guest_count"]}\nТип столика: {kwargs["table_type"]}\n' \
                      f'Особые пожелания: {kwargs["special_requests"]}\nИмя: {kwargs["first_name"]}\nТелефон: {kwargs["phone"]}'
            label = QLabel(details)
            layout.addWidget(label)
        elif action == "delete":
            details = f'Удалены данные блюда:\nДата: {kwargs["date"]}\nВремя: {kwargs["time"]}\n' \
                      f'Количество гостей: {kwargs["guest_count"]}\nТип столика: {kwargs["table_type"]}\n' \
                      f'Особые пожелания: {kwargs["special_requests"]}\nИмя: {kwargs["first_name"]}\nТелефон: {kwargs["phone"]}'
            label = QLabel(details)
            layout.addWidget(label)
            reason_label = QLabel("Причина удаления:")
            self.reason_combobox = QComboBox()
            self.reason_combobox.addItems(["Клиенты поели", "Отмена бронирования", "Другая причина"])
            layout.addWidget(reason_label)
            layout.addWidget(self.reason_combobox)

        buttons = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel)
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)
        layout.addWidget(buttons)

        self.setLayout(layout)

    def get_selected_reason(self):
        if hasattr(self, 'reason_combobox'):
            return self.reason_combobox.currentText()
        else:
            return None


class ManagerReservationWindow(QWidget):
    def __init__(self, current_user):
        super().__init__()
        self.current_user = current_user
        self.setWindowTitle('Управление бронью')
        self.setGeometry(100, 100, 800, 600)
        self.type_tables = list(MAX_TABLES.keys())
        self.initUI()
        self.action = None

    def initUI(self):
        layout = QVBoxLayout()

        self.table = QTableWidget(0, len(column_names_reservation))
        self.table.setHorizontalHeaderLabels(column_names_reservation)
        self.table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.table.setSelectionMode(QTableWidget.SelectionMode.SingleSelection)
        self.table.verticalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Interactive)

        header = self.table.horizontalHeader()
        for i in range(len(column_names_reservation)):
            header.setSectionResizeMode(i, QHeaderView.ResizeMode.Stretch)

        btn_layout = QHBoxLayout()
        self.btnAddReservation = QPushButton('Добавить', self)
        self.btnDeleteReservation = QPushButton('Удалить', self)
        self.btnSaveChanges = QPushButton('Сохранить изменения')
        self.load_reservation()

        self.table.setSortingEnabled(True)
        self.table.sortItems(0, Qt.SortOrder.AscendingOrder)

        btn_layout.addWidget(self.btnAddReservation)
        btn_layout.addWidget(self.btnDeleteReservation)
        btn_layout.addWidget(self.btnSaveChanges)

        self.btnAddReservation.clicked.connect(self.add_reservation)
        self.btnDeleteReservation.clicked.connect(self.delete_reservation)
        self.btnSaveChanges.clicked.connect(self.save_reservation)

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

        self.btnAddReservation.setStyleSheet("QPushButton {background-color: #32CD32; color: white;}")
        self.btnDeleteReservation.setStyleSheet("QPushButton {background-color: #FF6347; color: white;}")
        self.btnSaveChanges.setStyleSheet("QPushButton {background-color: #5CACEE; color: white;}")

    def load_reservation(self):
        self.table.setSortingEnabled(False)
        self.table.setRowCount(0)

        reservations = session.query(Reservation).all()
        for reservation in reservations:
            row_position = self.table.rowCount()
            self.table.insertRow(row_position)

            id_item = QTableWidgetItem(str(reservation.id))
            id_item.setFlags(id_item.flags() & ~Qt.ItemFlag.ItemIsEditable)
            self.table.setItem(row_position, 0, id_item)

            date_edit = QDateEdit(QDate.fromString(reservation.date, "yyyy-MM-dd"))
            date_edit.setDisplayFormat("yyyy-MM-dd")
            self.table.setCellWidget(row_position, 1, date_edit)
            date_edit.setCalendarPopup(True)
            time_edit = QTimeEdit(QTime.fromString(reservation.time, "HH:mm"))
            time_edit.setDisplayFormat("HH:mm")
            time_edit.setMinimumTime(QTime(START_TIME[0], START_TIME[1]))
            time_edit.setMaximumTime(QTime(END_TIME[0], END_TIME[1]))
            self.table.setCellWidget(row_position, 2, time_edit)

            fields = [reservation.guest_count, reservation.table_type,
                      reservation.special_requests, reservation.first_name, reservation.phone]
            for i, field in enumerate(fields, start=3):
                if i != 4:
                    item = QTableWidgetItem(str(field))
                    item.setFlags(item.flags() | Qt.ItemFlag.ItemIsEditable)
                    self.table.setItem(row_position, i, item)
                else:
                    combo_box = QComboBox()
                    combo_box.addItems(self.type_tables)
                    combo_box.setCurrentText(reservation.table_type)
                    combo_box.setEditable(True)
                    self.table.setCellWidget(row_position, i, combo_box)

            self.table.setSortingEnabled(True)
            self.table.sortItems(0, Qt.SortOrder.AscendingOrder)

    def add_reservation(self):
        row_position = self.table.rowCount()
        self.table.insertRow(row_position)
        date_edit = QDateEdit(QDate.fromString(datetime.now().strftime('%Y-%m-%d'), "yyyy-MM-dd"))
        date_edit.setDisplayFormat("yyyy-MM-dd")
        self.table.setCellWidget(row_position, 1, date_edit)
        date_edit.setCalendarPopup(True)
        time_edit = QTimeEdit(QTime.fromString(datetime.now().strftime('%H:%M'), "HH:mm"))
        time_edit.setDisplayFormat("HH:mm")
        time_edit.setMinimumTime(QTime(START_TIME[0], START_TIME[1]))
        time_edit.setMaximumTime(QTime(END_TIME[0], END_TIME[1]))
        self.table.setCellWidget(row_position, 2, time_edit)
        for i in range(3, len(column_names_reservation)):
            if i != 4:
                self.table.setItem(row_position, i, QTableWidgetItem(""))
            else:
                combo_box = QComboBox()
                combo_box.addItems(self.type_tables)
                self.table.setCellWidget(row_position, i, combo_box)
                self.table.editItem(self.table.item(row_position, 1))
        self.action = 'add'

    def save_reservation(self):
        row_count = self.table.currentRow()
        if row_count != -1:
            date_edit = self.table.cellWidget(row_count, 1)
            date = date_edit.date().toString("yyyy-MM-dd")
            time_edit = self.table.cellWidget(row_count, 2)
            time = time_edit.time().toString("HH:mm")
            guest_count = self.table.item(row_count, 3).text()
            table_types = self.table.cellWidget(row_count, 4)
            table_type = table_types.currentText()
            special_requests = self.table.item(row_count, 5).text()
            first_name = self.table.item(row_count, 6).text()
            phone = self.table.item(row_count, 7).text()

            if not guest_count.isdigit():
                QMessageBox.warning(self, "Ошибка", "Количество гостей должно содержать только цифры.")
                return
            if not table_type:
                QMessageBox.warning(self, "Ошибка", "Пожалуйста, напишите тип столика.")
                return
            if not self.is_table_available(date, time, table_type):
                QMessageBox.warning(self, "Ошибка", f"На это время все столики {table_type} уже забронированы.")
                return
            if not first_name or not all(char.isalpha() for char in first_name) or not all(
                    char in RUSSIAN_ALPHABET for char in first_name.lower()):
                QMessageBox.critical(self, "Ошибка", "Имя должно содержать только буквы русского алфавита.")
                return
            if not (phone.startswith('+7') or phone.startswith('8')) or len(phone.strip('+')) != 11 or not phone.strip('+').isdigit():
                QMessageBox.critical(self, "Ошибка", "Телефон должен начинаться на +7 или 8 и содержать 11 цифр.")
                return

            guest_count = int(guest_count)

            if self.action == 'add':
                dialog = ReservationInfoDialog('add', date=date, time=time, guest_count=guest_count,
                                               table_type=table_type,
                                               special_requests=special_requests, first_name=first_name, phone=phone)
                result = dialog.exec()
                if result == QDialog.DialogCode.Accepted:
                    new_user = Reservation(date=date, time=time, guest_count=guest_count, table_type=table_type,
                                           special_requests=special_requests, first_name=first_name, phone=phone)
                    session.add(new_user)
                    session.commit()

                    journal = Journal(action='add', time=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                                      details=f'Добавление брони от имени: {first_name}',
                                      first_name=self.current_user.first_name, last_name=self.current_user.last_name,
                                      role=self.current_user.role)
                    session.add(journal)
                    session.commit()
                    QMessageBox.information(self, "Успех", "Бронь успешно добавлена.")
                self.action = None
            else:
                reservation_id = int(self.table.item(row_count, 0).text())
                dialog = ReservationInfoDialog('edit', date=date, time=time, guest_count=guest_count,
                                               table_type=table_type,
                                               special_requests=special_requests, first_name=first_name, phone=phone)
                result = dialog.exec()
                if result == QDialog.DialogCode.Accepted:
                    self.update_reservation(reservation_id, date=date, time=time, guest_count=guest_count,
                                            table_type=table_type, special_requests=special_requests,
                                            first_name=first_name, phone=phone)
                    journal = Journal(action='edit', time=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                                      details=f'Изменение брони с ID: {reservation_id}',
                                      first_name=self.current_user.first_name, last_name=self.current_user.last_name,
                                      role=self.current_user.role)
                    session.add(journal)
                    session.commit()
                    QMessageBox.information(self, "Успех", "Бронь успешно изменена.")
            self.load_reservation()
        else:
            QMessageBox.warning(self, "Внимание", "Пожалуйста, выберите бронь.")
            return

    def update_reservation(self, reservation_id, date, time, guest_count, table_type, special_requests, first_name,
                           phone):
        try:
            reservation = session.query(Reservation).filter(Reservation.id == reservation_id).first()
            if reservation:
                reservation.date = date
                reservation.time = time
                reservation.guest_count = guest_count
                reservation.table_type = table_type
                reservation.special_requests = special_requests
                reservation.first_name = first_name
                reservation.phone = phone
                session.commit()
            else:
                QMessageBox.information(self, 'Ошибка', f'Бронь с ID: {reservation_id} не найдена.')
        except SQLAlchemyError as e:
            print("Ошибка при обновлении брони:", e)
            session.rollback()
            QMessageBox.information(self, 'Ошибка', f'Ошибка при обновлении брони: {e}')
            return

    def delete_reservation(self):
        current_row = self.table.currentRow()
        if current_row != -1:
            reservation_id = int(self.table.item(current_row, 0).text())
            reservation = session.query(Reservation).filter(Reservation.id == reservation_id).first()
            dialog = ReservationInfoDialog('delete', date=reservation.date, time=reservation.time,
                                           guest_count=reservation.guest_count, table_type=reservation.table_type,
                                           special_requests=reservation.special_requests,
                                           first_name=reservation.first_name,
                                           phone=reservation.phone)
            result = dialog.exec()

            if result == QDialog.DialogCode.Accepted:
                try:
                    session.delete(reservation)
                    session.commit()

                    selected_reason = dialog.get_selected_reason().lower()

                    self.table.removeRow(current_row)

                    journal = Journal(action='delete', time=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                                      details=f'Удаление брони по причине: {selected_reason} с данными:\nДата: {reservation.date}\nВремя: {reservation.time}\n' \
                                              f'Количество гостей: {reservation.guest_count}\nТип столика: {reservation.table_type}\n' \
                                              f'Особые пожелания: {reservation.special_requests}\nИмя: {reservation.first_name}\nТелефон: {reservation.phone}',
                                      first_name=self.current_user.first_name, last_name=self.current_user.last_name,
                                      role=self.current_user.role)
                    session.add(journal)
                    session.commit()

                    QMessageBox.information(self, "Успех", "Бронь успешно удалена.")
                except Exception as e:
                    QMessageBox.critical(self, "Ошибка", f"Не удалось удалить бронь: {e}")
                    session.rollback()
        else:
            QMessageBox.warning(self, "Внимание", "Пожалуйста, выберите бронь.")

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

    def sort_table(self, column):
        self.table.sortItems(column)


class ManagerStaffWindow(QWidget):
    def __init__(self, current_user):
        super().__init__()
        self.current_user = current_user
        self.setWindowTitle('Управление персоналом')
        self.setGeometry(100, 100, 800, 600)
        self.roles = ['client', 'waiter']
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
            User.role != 'admin' and User.role != 'manager').all()
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


class DishInfoDialog(QDialog):
    def __init__(self, action, **kwargs):
        super().__init__()
        self.setWindowTitle("Информация о блюде")
        layout = QVBoxLayout(self)

        if action == "add":
            details = f'Добавлено новое блюдо:\nНазвание: {kwargs["name"]}\nОписание: {kwargs["description"]}\n' \
                      f'Путь к изображению: {kwargs["photo_path"]}\nЦена: {kwargs["price"]}\nТип: {kwargs["type"]}\n'
        elif action == "edit":
            details = f'Изменены данные блюда:\nНазвание: {kwargs["name"]}\nОписание: {kwargs["description"]}\n' \
                      f'Путь к изображению: {kwargs["photo_path"]}\nЦена: {kwargs["price"]}\nТип: {kwargs["type"]}\n'
        elif action == "delete":
            details = f'Удалены данные блюда:\nНазвание: {kwargs["name"]}\nОписание: {kwargs["description"]}\n' \
                      f'Путь к изображению: {kwargs["photo_path"]}\nЦена: {kwargs["price"]}\nТип: {kwargs["type"]}\n'

        label = QLabel(details)
        layout.addWidget(label)

        buttons = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel)
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)
        layout.addWidget(buttons)

        self.setLayout(layout)


class ManagerMenuWindow(QWidget):
    def __init__(self, current_user):
        super().__init__()
        self.current_user = current_user
        self.setWindowTitle('Управление меню')
        self.setGeometry(100, 100, 800, 600)
        self.photo_paths = [f for f in os.listdir('image') if os.path.isfile(os.path.join('image', f))]
        self.text_edits = {}
        self.initUI()
        self.action = None

    def initUI(self):
        layout = QVBoxLayout()

        self.table = QTableWidget(0, len(column_names_menu))
        self.table.setHorizontalHeaderLabels(column_names_menu)
        self.table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.table.setSelectionMode(QTableWidget.SelectionMode.SingleSelection)
        self.table.verticalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Interactive)

        header = self.table.horizontalHeader()
        for i in range(len(column_names_menu)):
            header.setSectionResizeMode(i, QHeaderView.ResizeMode.Stretch)

        btn_layout = QHBoxLayout()
        self.btnAddDish = QPushButton('Добавить', self)
        self.btnDeleteDish = QPushButton('Удалить', self)
        self.btnSaveChanges = QPushButton('Сохранить изменения')
        self.load_menu()

        self.table.setSortingEnabled(True)
        self.table.sortItems(0, Qt.SortOrder.AscendingOrder)

        btn_layout.addWidget(self.btnAddDish)
        btn_layout.addWidget(self.btnDeleteDish)
        btn_layout.addWidget(self.btnSaveChanges)

        self.btnAddDish.clicked.connect(self.add_dish)
        self.btnDeleteDish.clicked.connect(self.delete_user)
        self.btnSaveChanges.clicked.connect(self.save_dish)

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

        self.btnAddDish.setStyleSheet("QPushButton {background-color: #32CD32; color: white;}")
        self.btnDeleteDish.setStyleSheet("QPushButton {background-color: #FF6347; color: white;}")
        self.btnSaveChanges.setStyleSheet("QPushButton {background-color: #5CACEE; color: white;}")

    def load_menu(self):
        self.table.setSortingEnabled(False)
        self.table.setRowCount(0)

        menu = session.query(MenuItem).all()
        for dish in menu:
            row_position = self.table.rowCount()
            self.table.insertRow(row_position)

            id_item = QTableWidgetItem(str(dish.id))
            id_item.setFlags(id_item.flags() & ~Qt.ItemFlag.ItemIsEditable)
            self.table.setItem(row_position, 0, id_item)

            fields = [dish.name, dish.description, dish.photo_path, dish.price, dish.type]
            for i, field in enumerate(fields, start=1):
                if i == 2:
                    text_edit = QTextEdit(str(field))
                    self.table.setCellWidget(row_position, i, text_edit)
                    self.table.horizontalHeader().setSectionResizeMode(i, QHeaderView.ResizeMode.Stretch)
                    self.text_edits[(row_position, i)] = text_edit
                if i == 3:
                    combo_box = QComboBox()
                    combo_box.addItems(self.photo_paths)
                    combo_box.setCurrentText(dish.photo_path)
                    combo_box.setEditable(True)
                    self.table.setCellWidget(row_position, i, combo_box)
                    self.table.horizontalHeader().setSectionResizeMode(i, QHeaderView.ResizeMode.ResizeToContents)
                else:
                    item = QTableWidgetItem(str(field))
                    item.setFlags(item.flags() | Qt.ItemFlag.ItemIsEditable)
                    self.table.setItem(row_position, i, item)
                    self.table.horizontalHeader().setSectionResizeMode(i, QHeaderView.ResizeMode.ResizeToContents)

            self.table.setSortingEnabled(True)
            self.table.sortItems(0, Qt.SortOrder.AscendingOrder)

    def add_dish(self):
        row_position = self.table.rowCount()
        self.table.insertRow(row_position)
        for i in range(1, len(column_names_menu)):
            if i == 2:
                text_edit = QTextEdit('')
                self.table.setCellWidget(row_position, i, text_edit)
                self.table.horizontalHeader().setSectionResizeMode(i, QHeaderView.ResizeMode.Stretch)
                self.text_edits[(row_position, i)] = text_edit
            if i == 3:
                combo_box = QComboBox()
                combo_box.addItems(self.photo_paths)
                combo_box.setEditable(True)
                self.table.setCellWidget(row_position, i, combo_box)
                self.table.horizontalHeader().setSectionResizeMode(i, QHeaderView.ResizeMode.ResizeToContents)
            else:
                item = QTableWidgetItem('')
                item.setFlags(item.flags() | Qt.ItemFlag.ItemIsEditable)
                self.table.setItem(row_position, i, item)
                self.table.horizontalHeader().setSectionResizeMode(i, QHeaderView.ResizeMode.ResizeToContents)
        self.action = 'add'

    def save_dish(self):
        row_count = self.table.currentRow()
        if row_count != -1:
            name = self.table.item(row_count, 1).text()
            description = self.text_edits.get((row_count, 2)).toPlainText()
            photo_combo = self.table.cellWidget(row_count, 3)
            photo_path = photo_combo.currentText()
            price = self.table.item(row_count, 4).text()
            type_ = self.table.item(row_count, 5).text().lower()

            if not name:
                QMessageBox.warning(self, "Ошибка", "Пожалуйста, напишите название.")
                return
            if not description:
                QMessageBox.warning(self, "Ошибка", "Пожалуйста, напишите описание.")
                return
            if not price or not price.isdigit():
                QMessageBox.warning(self, "Ошибка", "Пожалуйста, напишите цену.")
                return
            if not type_:
                QMessageBox.warning(self, "Ошибка", "Пожалуйста, напишите тип.")
                return

            if self.action == 'add':
                if self.dish_exists(name, photo_path):
                    QMessageBox.critical(self, "Ошибка", "Блюдо с такими данными уже существует.")
                    return
                dialog = DishInfoDialog('add', name=name, description=description, photo_path=photo_path, price=price,
                                        type=type_)
                result = dialog.exec()
                if result == QDialog.DialogCode.Accepted:
                    new_user = MenuItem(name=name, description=description, photo_path=photo_path, price=price,
                                        type=type_)
                    session.add(new_user)
                    session.commit()

                    journal = Journal(action='add', time=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                                      details=f'Добавление блюда с названием: {name}',
                                      first_name=self.current_user.first_name, last_name=self.current_user.last_name,
                                      role=self.current_user.role)
                    session.add(journal)
                    session.commit()
                    QMessageBox.information(self, "Успех", "Блюдо успешно добавлено.")
                self.action = None
            else:
                dish_id = int(self.table.item(row_count, 0).text())
                dialog = DishInfoDialog('edit', name=name, description=description, photo_path=photo_path, price=price,
                                        type=type_)
                result = dialog.exec()
                if result == QDialog.DialogCode.Accepted:
                    self.update_dish(dish_id, name, description, photo_path, price, type_)
                    journal = Journal(action='edit', time=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                                      details=f'Изменение блюда с ID: {dish_id}',
                                      first_name=self.current_user.first_name, last_name=self.current_user.last_name,
                                      role=self.current_user.role)
                    session.add(journal)
                    session.commit()
                    QMessageBox.information(self, "Успех", "Блюдо успешно изменено.")
            self.load_menu()
        else:
            QMessageBox.warning(self, "Внимание", "Пожалуйста, выберите пользователя.")
            return

    def update_dish(self, dish_id, name, description, photo_path, price, type):
        try:
            menu = session.query(MenuItem).filter(MenuItem.id == dish_id).first()
            if menu:
                menu.name = name
                menu.description = description
                menu.photo_path = photo_path
                menu.price = price
                menu.type = type
                session.commit()
            else:
                QMessageBox.information(self, 'Ошибка', f'Блюдо с ID: {dish_id} не найдено.')
        except SQLAlchemyError as e:
            print("Ошибка при обновлении блюда:", e)
            session.rollback()
            QMessageBox.information(self, 'Ошибка', f'Ошибка при обновлении блюда: {e}')
            return

    def delete_user(self):
        current_row = self.table.currentRow()
        if current_row != -1:
            dish_id = int(self.table.item(current_row, 0).text())
            menu = session.query(MenuItem).filter(MenuItem.id == dish_id).first()
            dialog = DishInfoDialog('delete', name=menu.name, description=menu.description, photo_path=menu.photo_path,
                                    price=menu.price, type=menu.type)
            result = dialog.exec()

            if result == QDialog.DialogCode.Accepted:
                try:
                    session.delete(menu)
                    session.commit()

                    self.table.removeRow(current_row)

                    journal = Journal(action='delete', time=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                                      details=f'Удаление блюда с данными:\nНазвание: {menu.name}\nОписание: {menu.description}\n' \
                                              f'Путь к изображению: {menu.photo_path}\nЦена: {menu.price}\nТип: {menu.type}\n',
                                      first_name=self.current_user.first_name, last_name=self.current_user.last_name,
                                      role=self.current_user.role)
                    session.add(journal)
                    session.commit()

                    QMessageBox.information(self, "Успех", "Блюдо успешно удалено.")
                except Exception as e:
                    QMessageBox.critical(self, "Ошибка", f"Не удалось удалить блюдо: {e}")
                    session.rollback()
        else:
            QMessageBox.warning(self, "Внимание", "Пожалуйста, выберите блюдо.")

    def dish_exists(self, name, photo_path):
        menu = session.query(User).filter(
            (MenuItem.name == name) | (MenuItem.photo_path == photo_path)).first()
        return menu is not None

    def sort_table(self, column):
        self.table.sortItems(column)
