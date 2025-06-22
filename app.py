import sys
import os
import shutil
from PySide6.QtWidgets import *
from PySide6.QtGui import *
from PySide6.QtCore import *

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
        layout.addWidget(btn)
        self.setLayout(layout)

    def accept(self):
        # Define file extensions
        image_extension = (".jpg", ".jpeg", ".png", ".gif")
        video_extension = (".mp4", ".mov", ".webm", ".mkv")
        document_extension = (".doc", ".docx", ".odt", ".pdf", ".txt", "pptx")
        code_extension = (".py", ".js", ".html", ".css")
        audio_extension = (".mp3", ".wav", ".aiff", ".flac", ".aac")

        global selected_folder
        ddir = selected_folder

        subdirectories = ["Images", "Videos", "Documents", "Code", "Audio", "Others"]
        for subdirectory in subdirectories:
            path = os.path.join(ddir, subdirectory)
            if not os.path.exists(path):
                os.makedirs(path)

        def get_images(file): return os.path.splitext(file)[1].lower() in image_extension
        def get_videos(file): return os.path.splitext(file)[1].lower() in video_extension
        def get_document(file): return os.path.splitext(file)[1].lower() in document_extension
        def get_code(file): return os.path.splitext(file)[1].lower() in code_extension
        def get_audio(file): return os.path.splitext(file)[1].lower() in audio_extension

        for file in os.listdir(ddir):
            file_path = os.path.join(ddir, file)
            if os.path.isdir(file_path):
                continue
            try:
                if get_images(file):
                    shutil.move(file_path, os.path.join(ddir, "Images", file))
                elif get_videos(file):
                    shutil.move(file_path, os.path.join(ddir, "Videos", file))
                elif get_document(file):
                    shutil.move(file_path, os.path.join(ddir, "Documents", file))
                elif get_code(file):
                    shutil.move(file_path, os.path.join(ddir, "Code", file))
                elif get_audio(file):
                    shutil.move(file_path, os.path.join(ddir, "Audio", file))
                else:
                    shutil.move(file_path, os.path.join(ddir, "Others", file))
            except Exception as e:
                print(f"Error moving {file}: {e}")

        print("File organization complete!")
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
                     "6. Files will be moved to their respective folders based on their extensions."))
        layout.addWidget(ok_button)
        self.setLayout(layout)

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("4o")
        icon_path = os.path.join(getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__))), "4o_icon.ico")
        self.setWindowIcon(QIcon(icon_path))

        self.resize(QSize(200, 200))

        layout = QVBoxLayout()
        button = QPushButton("Open Folder")
        button.setFixedSize(QSize(200, 150))
        button.setToolTip("Click to select a folder for file organization")
        button.clicked.connect(self.openFolder)
        layout.addWidget(button)

        instructions = QPushButton("Instructions")
        instructions.setToolTip("Click to open instructions")
        instructions.setFixedSize(QSize(200, 50))
        instructions.clicked.connect(self.showInstructions)
        layout.addWidget(instructions)

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
        
        
app = QApplication([])

window = MainWindow()
window.show()

app.exec()
