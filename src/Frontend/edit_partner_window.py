from PyQt6.QtWidgets import QDialog, QVBoxLayout, QLabel, QFormLayout, QComboBox, QLineEdit, QPushButton, QHBoxLayout
from alembic.command import history
from PyQt6.QtCore import Qt, pyqtSignal
from Backend.crud_operations import get_partner_types, get_partner_by_name, edit_partner
from database.session import session

class EditPartnerWindow(QDialog):
    partner_edited = pyqtSignal()

    def __init__(self, data):
        super().__init__()
        self.setFixedSize(900, 700)
        self.setModal(True)
        main_layout = QVBoxLayout()
        # ====================
        self.partner_data = data

        form_layout = QFormLayout()
        self.partner_type = QComboBox()
        self.partner_type.addItems(get_partner_types())
        self.partner_type.setCurrentText(data['partner_type'])
        self.partner_name = QLineEdit(data['partner_name'])
        self.director = QLineEdit(data['director'])
        self.phone_number = QLineEdit(data['phone'])
        self.rating = QLineEdit(str(data['rating']))

        partner = get_partner_by_name(data['partner_name'])


        self.address = QLineEdit(partner.address)
        self.email = QLineEdit(partner.email)
        self.INN = QLineEdit(partner.INN)
        form_layout.addRow("Тип партнера:", self.partner_type)
        form_layout.addRow("Наименование партнера:", self.partner_name)
        form_layout.addRow("Директор:", self.director)
        form_layout.addRow("Эл. почта:", self.email)
        form_layout.addRow("Номер телефона:", self.phone_number)
        form_layout.addRow("Адрес:", self.address)
        form_layout.addRow("ИНН:", self.INN)
        form_layout.addRow("Рейтинг:", self.rating)
        self.not_label = QLabel("")
        main_layout.addLayout(form_layout)
        main_layout.addWidget(self.not_label)
        accept_button = QPushButton("OK")
        accept_button.clicked.connect(self.partner_edit)

        self.partner = get_partner_by_name(self.partner_name.text())

        close_button = QPushButton("Cancel")
        close_button.clicked.connect(self.reject)

        button_layout = QHBoxLayout()
        button_layout.addWidget(accept_button)
        button_layout.addWidget(close_button)

        main_layout.addLayout(button_layout)

        # ====================
        self.setLayout(main_layout)

    def partner_edit(self):
        p_type = (self.partner_type.currentText())
        name = self.partner_name.text()
        director = self.director.text()
        email = self.email.text()
        phone = self.phone_number.text()
        address = self.address.text()
        inn = self.INN.text()
        rating = self.rating.text()
        p_id = self.partner.id
        if p_type and name and director and email and phone and address and inn and rating:
            if rating.isdigit():
                if int(rating) > 0 and int(rating) < 11:
                    query = edit_partner(p_id, p_type, name, director, email, phone, address, inn, int(rating))
                    if query == 0:
                        self.not_label.setText("Пользователь успешно обновлен")
                        self.partner_edited.emit()
                        self.accept()
                    else:
                        self.not_label.setText(f"Ошибка при изменении пользователя.\n Код ошибки: {query}")
                else:
                    self.not_label.setText("Укажите целочисленное значение рейтинга\nот 0 до 10")
            else:
                self.not_label.setText("Укажите целочисленное значение рейтинга\nот 0 до 10")
        else:
            self.not_label.setText("Заполните все поля")