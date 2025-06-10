from PySide6.QtWidgets import QApplication, QMainWindow, QFileDialog, QPushButton

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("4o")
        self.resize(400, 600)

        button = QPushButton("Open File")
        self.setCentralWidget(button)
        button.clicked.connect(self.open_folder)

    def open_folder(self):
        folder = QFileDialog.getExistingDirectory(self, "Select Folder", "")
        print(f"Selected file: {folder}")

app = QApplication([])

window = MainWindow()
window.show()

app.exec()
