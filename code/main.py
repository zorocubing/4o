import os
import shutil

# Define file extensions
image_extension = (".jpg", ".jpeg", ".png", ".gif")
video_extension = (".mp4", ".mov", ".webm", ".mkv")
document_extension = (".doc", ".docx", ".odt", ".pdf")
code_extension = (".py", ".js", ".html", ".css")

# Downloads directory
ddir = "/Users/kanso/Downloads"

# Create subdirectories if they don't exist
subdirectories = ["Images", "Videos", "Documents", "Code", "Others"]
for subdirectory in subdirectories:
    path = os.path.join(ddir, subdirectory)
    if not os.path.exists(path):
        os.makedirs(path)


# Helper functions to check file types
def get_images(file):
    return os.path.splitext(file)[1].lower() in image_extension


def get_videos(file):
    return os.path.splitext(file)[1].lower() in video_extension


def get_document(file):
    return os.path.splitext(file)[1].lower() in document_extension


def get_code(file):
    return os.path.splitext(file)[1].lower() in code_extension


# Iterate through files in the Downloads directory
for file in os.listdir(ddir):
    file_path = os.path.join(ddir, file)

    # Skip directories
    if os.path.isdir(file_path):
        continue

    # Move files to appropriate folders
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