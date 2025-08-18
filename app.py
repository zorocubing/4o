import sys
import os
import shutil
from PySide6.QtWidgets import *
from PySide6.QtGui import *
from PySide6.QtCore import *
import files

selected_folder = None

class ConfirmDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.setWindowTitle("Confirmation")
        icon_path = os.path.join(getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__))), "4o_icon.ico")
        self.setWindowIcon(QIcon(icon_path))
        self.setBaseSize(100, 100)

        btn = QDialogButtonBox(QDialogButtonBox.Yes | QDialogButtonBox.No)
        btn.accepted.connect(self.accept)
        btn.rejected.connect(self.reject)
        btn.setCenterButtons(True)

        layout = QVBoxLayout()
        layout.addWidget(QLabel(f"Do you want to organize {selected_folder}?"))
        layout.addWidget(QLabel("Note: This is irreversible."))
        layout.addWidget(btn)
        self.setLayout(layout)

    def accept(self):
        files.organize_files(selected_folder)
        ConfirmDialog.close(self)
        dlg = QDialog(self)
        dlg.setWindowTitle("Success")
        success_btn = QDialogButtonBox(QDialogButtonBox.Ok)
        success_btn.setCenterButtons(True)
        success_btn.accepted.connect(dlg.accept)
        layout = QVBoxLayout(dlg)
        layout.addWidget(QLabel("Files organization complete! \n" "Check your Files Explorer app!"))
        layout.addWidget(success_btn)
        dlg.setLayout(layout)
        icon_path = os.path.join(getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__))), "4o_icon.ico")
        dlg.setWindowIcon(QIcon(icon_path))
        dlg.exec()
        super().accept()

class InstructionsDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Instructions")
        icon_path = os.path.join(getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__))), "4o_icon.ico")
        self.setWindowIcon(QIcon(icon_path))
        ok_button = QDialogButtonBox(QDialogButtonBox.Ok)
        ok_button.setCenterButtons(True)
        ok_button.accepted.connect(self.accept)
        layout = QVBoxLayout(self)
        layout.addWidget(QLabel("How to use the application:"))
        layout.addWidget(QLabel("1. Click 'Open Folder' to select a folder. \n"
                     "2. After selecting, a confirmation window will appear. \n"
                     "3. Click 'Yes' to organize files into respective folders. \n"
                     "4. Click 'No' to cancel the operation. \n"
                     "5. The application will create subfolders for Images, Videos, Documents, Code, Audio, and Others. \n"
                     "6. Files will be moved to their respective folders based on their extensions. \n"
                     "7. Check the organized output in your Files Explorer app!"))
        layout.addWidget(ok_button)
        self.setLayout(layout)

class RedoDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Redo")
        icon_path = os.path.join(getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__))), "4o_icon.ico")
        self.setWindowIcon(QIcon(icon_path))
        ok_button = QDialogButtonBox(QDialogButtonBox.Ok)
        ok_button.setCenterButtons(True)
        ok_button.accepted.connect(self.accept)
        layout = QVBoxLayout(self)
        layout.addWidget(QLabel("This feature is coming soon!"))
        layout.addWidget(ok_button)
        self.setLayout(layout)

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("4o")
        icon_path = os.path.join(getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__))), "4o_icon.ico")
        self.setWindowIcon(QIcon(icon_path))
        self.setMaximumSize(QSize(200, 200))

        layout = QVBoxLayout()
        hlayout = QHBoxLayout()


        button = QPushButton("Open Folder")
        button.setMinimumSize(QSize(200, 150))
        button.setToolTip("Click to select a folder for files organization")
        button.clicked.connect(self.openFolder)
        layout.addWidget(button)

        instructions = QPushButton("ℹ️")
        instructions.setMinimumSize(QSize(100, 50))
        instructions.setToolTip("Click to open instructions")
        instructions.clicked.connect(self.showInstructions)
        hlayout.addWidget(instructions)

        redo = QPushButton("↩️")
        redo.setMinimumSize(QSize(100, 50))
        redo.setStyleSheet("""
        QPushButton {
            background-color: #c9184a;
        }
        QPushButton:hover {
            background-color: #b71744;
            border-radius: 5px;
        }
        """)
        redo.setToolTip("Click to redo the last operation")
        redo.clicked.connect(self.redo)
        hlayout.addWidget(redo)

        layout.addLayout(hlayout)
        self.setwatermark = QLabel("v1.3 Beta")
        self.setwatermark.setAlignment(Qt.AlignCenter)
        self.setwatermark.setStyleSheet("color: gray; font-size: 10px;")
        self.setwatermark.setMinimumSize(QSize(200, 10))
        layout.addWidget(self.setwatermark)

        w = QWidget()
        w.setLayout(layout)
        self.setCentralWidget(w)

    def showInstructions(self):
        InstructionsDialog(self).exec()
        

    def openFolder(self):
        global selected_folder
        dialog = QFileDialog(self)
        dialog.setFileMode(QFileDialog.Directory)
        dialog.setOption(QFileDialog.ShowDirsOnly, False)
        dialog.setOption(QFileDialog.DontUseNativeDialog, True)
        dialog.setWindowTitle("Select Folder")
        if dialog.exec():
            folder = dialog.selectedFiles()[0]
            selected_folder = folder
            print(f"Selected folder: {folder}")
            
            # Trigger the ConfirmDialog here
            confirm = ConfirmDialog(self)
            if confirm.exec():
                print("User confirmed file organization.")
        else:
            print("No folder selected.")

    def redo(self):
        RedoDialog(self).exec()