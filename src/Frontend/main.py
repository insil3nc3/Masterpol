from PyQt6.QtWidgets import QApplication
from main_window import Main_window

app = QApplication([])
window = Main_window()
window.show()
app.exec()