import os
from PySide6.QtWidgets import QWidget, QApplication, QMainWindow, QFileDialog, QPushButton

class ConfirmWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Child Window")
        self.resize(200, 100)
        self.setStyleSheet("background-color: lightblue;")
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("4o")
        self.resize(200, 200)

        button = QPushButton("Open Folder")
        self.setCentralWidget(button)
        button.clicked.connect(self.open_folder)

    def open_folder(self):
        folder = QFileDialog.getExistingDirectory(self, "Select Folder", "")
        print(f"Selected folder: {folder}")


app = QApplication([])

window = MainWindow()
window.show()

app.exec()