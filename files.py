import sys
import os
import shutil

def organize_files(ddir: str):
    # Define file extensions
    image_extension = (".jpg", ".jpeg", ".png", ".gif", ".ico")
    video_extension = (".mp4", ".mov", ".webm", ".mkv")
    document_extension = (".doc", ".docx", ".odt", ".pdf", ".txt", ".pptx", ".xlsx", ".csv")
    code_extension = (".py", ".js", ".html", ".css")
    audio_extension = (".mp3", ".wav", ".aiff", ".flac", ".aac")

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