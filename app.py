from PySide6.QtWidgets import QWidget, QApplication, QMainWindow, QFileDialog, QPushButton, QLabel, QDialog, QVBoxLayout, QDialogButtonBox
from PySide6.QtGui import QIcon


class ConfirmDialog(QDialog):
    def __init__(self,  parent=None):
        super().__init__()

        self.setWindowTitle("Confirmation")
        self.setIcon()
        self.resize(100, 100)
        btn = QDialogButtonBox(QDialogButtonBox.Yes | QDialogButtonBox.No)
        btn.accepted.connect(self.accept)
        btn.rejected.connect(self.reject)
        layout = QVBoxLayout()
        layout.addWidget(QLabel("   Do you want to proceed? "))
        layout.addWidget(btn)
        self.setLayout(layout)     

    def setIcon(self):
        icon = QIcon('4o_icon.png')
        self.setWindowIcon(icon)   

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("4o")
        self.setIcon()
        self.resize(200, 200)

        button = QPushButton("Open Folder")
        self.setCentralWidget(button)
        button.clicked.connect(self.openFolder)

    def setIcon(self):
        icon = QIcon('4o_icon.png')
        self.setWindowIcon(icon)
        

    def openFolder(self):
        folder = QFileDialog.getExistingDirectory(self, "Select Folder", "")
        if folder != "":
            print(f"Selected folder: {folder}")
            dlg = ConfirmDialog(self)
            dlg.exec()
        else:
            print("No folder selected")
        
        
        
app = QApplication([])

window = MainWindow()
window.show()

app.exec()