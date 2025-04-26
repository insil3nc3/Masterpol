from PyQt6.QtWidgets import QDialog, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QTableWidget, QLabel, \
    QTableWidgetItem, QHeaderView
from PyQt6.QtCore import Qt

from Backend.crud_operations import get_product_quantity, history_query

class HistoryWindow(QDialog):
    def __init__(self, data):
        super().__init__()
        self.data = data
        self.setFixedSize(900, 700)
        self.setModal(True)
        main_layout = QVBoxLayout()
        self.setLayout(main_layout)
        # ====================

        self.history_table = QTableWidget()

        self.populate_table()
        # populate_table() to refresh table
        main_layout.addWidget(self.history_table, stretch=1)

        back_button = QPushButton("Назад")
        back_button.clicked.connect(self.reject)
        main_layout.addWidget(back_button)


    def populate_table(self):
        self.history_table.clearContents()
        self.history_table.setColumnCount(3)
        products_quantity = get_product_quantity(self.data["partner_name"])
        self.history_table.setRowCount(products_quantity)
        data = history_query(self.data["partner_name"])
        for row in range(products_quantity):

            # 0=product_name, 1=quantity, 2=sell_data
            self.history_table.setHorizontalHeaderLabels(["Продукция", "Количество", "Дата продажи"])
            self.history_table.setItem(row, 0, QTableWidgetItem(data[row]["product_name"]))
            self.history_table.setItem(row, 1, QTableWidgetItem(str(data[row]["product_quantity"])))
            self.history_table.setItem(row, 2, QTableWidgetItem(data[row]["data"]))

        header = self.history_table.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.ResizeMode.Stretch)