import os
import shutil
from PySide6.QtWidgets import QWidget, QApplication, QMainWindow, QFileDialog, QPushButton, QLabel, QDialog, QVBoxLayout, QDialogButtonBox
from PySide6.QtGui import QIcon

selected_folder = None


class ConfirmDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)

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

    def accept(self):
        # Define file extensions
        image_extension = (".jpg", ".jpeg", ".png", ".gif")
        video_extension = (".mp4", ".mov", ".webm", ".mkv")
        document_extension = (".doc", ".docx", ".odt", ".pdf")
        code_extension = (".py", ".js", ".html", ".css")

        global selected_folder
        ddir = selected_folder

        subdirectories = ["Images", "Videos", "Documents", "Code", "Others"]
        for subdirectory in subdirectories:
            path = os.path.join(ddir, subdirectory)
            if not os.path.exists(path):
                os.makedirs(path)

        def get_images(file): return os.path.splitext(file)[1].lower() in image_extension
        def get_videos(file): return os.path.splitext(file)[1].lower() in video_extension
        def get_document(file): return os.path.splitext(file)[1].lower() in document_extension
        def get_code(file): return os.path.splitext(file)[1].lower() in code_extension

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
                else:
                    shutil.move(file_path, os.path.join(ddir, "Others", file))
            except Exception as e:
                print(f"Error moving {file}: {e}")

        print("File organization complete!")
        super().accept()

    def setIcon(self):
        icon = QIcon("4o_icon.ico")
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
        icon = QIcon("4o_icon.ico")
        self.setWindowIcon(icon)
        

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