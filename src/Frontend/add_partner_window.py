from PyQt6.QtCore import pyqtSignal
from PyQt6.QtWidgets import QPushButton, QVBoxLayout, QLineEdit, QComboBox, QDialog, QFormLayout, QHBoxLayout, QLabel
from Backend.crud_operations import get_partner_types, add_partner, get_partner_type_id_by_name

class AddPartnerWindow(QDialog):
    partner_added = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.setFixedSize(900, 700)
        self.setModal(True)
        main_layout = QVBoxLayout()
        # ====================
        form_layout = QFormLayout()
        self.partner_type = QComboBox()
        self.partner_type.addItems(get_partner_types())
        self.partner_name = QLineEdit()
        self.director = QLineEdit()
        self.phone_number = QLineEdit()
        self.rating = QLineEdit()
        self.address = QLineEdit()
        self.email = QLineEdit()
        self.INN = QLineEdit()

        form_layout.addRow("Тип партнера:", self.partner_type)
        form_layout.addRow("Наименование партнера:", self.partner_name)
        form_layout.addRow("Директор:", self.director)
        form_layout.addRow("Эл. почта:", self.email)
        form_layout.addRow("Номер телефона:", self.phone_number)
        form_layout.addRow("Адрес:", self.address)
        form_layout.addRow("ИНН:", self.INN)
        form_layout.addRow("Рейтинг:", self.rating)

        submit_button = QPushButton("ОК")
        submit_button.clicked.connect(self.add_partner)
        close_button = QPushButton("Cancel")
        close_button.clicked.connect(self.reject)

        self.not_label = QLabel("")
        # self.not_label.setText("")

        main_layout.addLayout(form_layout)
        button_layout = QHBoxLayout()
        button_layout.addWidget(close_button)
        button_layout.addWidget(submit_button)

        main_layout.addWidget(self.not_label)
        main_layout.addLayout(button_layout)

        self.setLayout(main_layout)

    def add_partner(self):
        p_type = (self.partner_type.currentText())
        name = self.partner_name.text()
        director = self.director.text()
        email = self.email.text()
        phone = self.phone_number.text()
        address = self.address.text()
        inn = self.INN.text()
        rating = self.rating.text()
        if p_type and name and director and email and phone and address and inn and rating:
            if rating.isdigit():
                if int(rating) > 0 and int(rating) < 11:
                    query = add_partner(p_type, name, director, email, phone, address, inn, int(rating))
                    if query == 0:
                        self.not_label.setText("Пользователь успешно добавлен")
                        self.partner_added.emit()
                        self.accept()
                    else:
                        self.not_label.setText(f"Ошибка при добавлении пользователя.\n Код ошибки: {query}")
                else:
                    self.not_label.setText("Укажите целочисленное значение рейтинга\nот 0 до 10")
            else:
                self.not_label.setText("Укажите целочисленное значение рейтинга\nот 0 до 10")
        else:
            self.not_label.setText("Заполните все поля")