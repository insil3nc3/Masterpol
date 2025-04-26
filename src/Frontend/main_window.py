from PyQt6.QtWidgets import QWidget, QMainWindow, QApplication, QPushButton, QListWidget, QListWidgetItem, QLabel, \
    QVBoxLayout, QHBoxLayout
from PyQt6.QtCore import Qt, QSize
from alembic.command import history
from setuptools.command.setopt import edit_config

from product_history_window import HistoryWindow
from edit_partner_window import EditPartnerWindow
from add_partner_window import AddPartnerWindow
from Backend.main_window import partners_info, get_partners_quantity
from Backend.crud_operations import delete_partner, get_partner_by_name


class Main_window(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setBaseSize(1100, 900)
        self.setWindowTitle("Masterpol")

        # ====================
        central_widget = QWidget()
        main_layout = QVBoxLayout()
        central_widget.setLayout(main_layout)
        # ====================

        # Label
        top_label = QLabel("Masterpol")
        main_layout.addWidget(top_label, alignment=Qt.AlignmentFlag.AlignHCenter)

        # LIST
        self.partners_list = QListWidget()
        #self.partners_list.setSelectionMode(QListWidget.SelectionMode.NoSelection)
        self.partners_list.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self.partners_list.itemDoubleClicked.connect(self.edit_partner)
        main_layout.addWidget(self.partners_list)

        self.partner_edit = None

        self.populate_list()
        # populate_list() to refresh data

        # Add Button
        history_button = QPushButton("История партнера")
        history_button.clicked.connect(self.open_history)
        main_layout.addWidget(history_button, alignment=Qt.AlignmentFlag.AlignLeft)

        button_layout = QHBoxLayout()

        add_partner_button = QPushButton("Добавить")
        add_partner_button.clicked.connect(self.partner_add)
        button_layout.addWidget(add_partner_button)

        del_partner = QPushButton("Удалить")
        del_partner.clicked.connect(self.delete_partner)
        button_layout.addWidget(del_partner)

        main_layout.addLayout(button_layout)
        self.add_partner = None
        self.history = None
        # ====================
        self.setCentralWidget(central_widget)

    def open_history(self):
        current_item = self.partners_list.currentItem()
        if current_item:
            data = current_item.data(Qt.ItemDataRole.UserRole)
            self.history = HistoryWindow(data)
            self.history.exec()

    def partner_add(self):
        self.add_partner = AddPartnerWindow()
        self.add_partner.partner_added.connect(self.populate_list)
        self.add_partner.exec()

    def edit_partner(self):
        current_item = self.partners_list.currentItem()
        data = current_item.data(Qt.ItemDataRole.UserRole)
        self.partner_edit = EditPartnerWindow(data)  # всегда создавай новое окно
        self.partner_edit.partner_edited.connect(self.populate_list)
        self.partner_edit.exec()  # открой как модальное

    def populate_card(self, data):

        item_widget = QWidget()
        item_layout = QVBoxLayout()

        label_layout = QHBoxLayout()
        item_widget.setLayout(item_layout)
        label_layout.addWidget(QLabel(f"{data["partner_type"]} | {data["partner_name"]}"), alignment=Qt.AlignmentFlag.AlignLeft)
        label_layout.addWidget(QLabel(f"{data["discount"]}%"), alignment=Qt.AlignmentFlag.AlignRight)
        item_layout.addLayout(label_layout)
        item_layout.addWidget(QLabel(data["director"]), alignment=Qt.AlignmentFlag.AlignLeft)
        item_layout.addWidget(QLabel(data["phone"]))
        item_layout.addWidget(QLabel(f"Рейтинг: {data["rating"]}"))

        item = QListWidgetItem()
        item.setSizeHint(item_widget.sizeHint())
        item.setData(Qt.ItemDataRole.UserRole, data)
        self.partners_list.addItem(item)
        self.partners_list.setItemWidget(item, item_widget)

    def populate_list(self):
        self.partners_list.clear()
        for i in range (1, (get_partners_quantity()+1)):
            data = partners_info(i)
            if data != -1:
                self.populate_card(data)

    def delete_partner(self):
        current_item = self.partners_list.currentItem()
        data = current_item.data(Qt.ItemDataRole.UserRole)
        partner = get_partner_by_name(data["partner_name"])
        user_del = delete_partner(partner.id)
        self.populate_list()