import os
import datetime

class FileInfo:
    def __init__(self, file_path):
        self.file_path = file_path
        self.filename, self.extension = os.path.splitext(file_path)
        self.created_time = datetime.datetime.fromtimestamp(os.path.getctime(file_path))
        self.updated_time = datetime.datetime.fromtimestamp(os.path.getmtime(file_path))

    def get_info(self):
        return f"{self.filename}{self.extension} - Unknown File Type"

class ImageFile(FileInfo):
    def get_info(self):
        size = os.path.getsize(self.file_path)
        return f"{self.filename}{self.extension} - Image File (Size: {size} bytes)"

class TextFile(FileInfo):
    def get_info(self):
        with open(self.file_path, 'r') as f:
            lines = f.readlines()
            line_count = len(lines)
            word_count = sum(len(line.split()) for line in lines)
            char_count = sum(len(line) for line in lines)
        return f"{self.filename}{self.extension} - Text File (Lines: {line_count}, Words: {word_count}, Characters: {char_count})"

class ProgramFile(FileInfo):
    def get_info(self):
        with open(self.file_path, 'r') as f:
            lines = f.readlines()
            line_count = len(lines)
            class_count = sum(1 for line in lines if line.strip().startswith('class '))
            method_count = sum(1 for line in lines if line.strip().startswith('def '))
        return f"{self.filename}{self.extension} - Program File (Lines: {line_count}, Classes: {class_count}, Methods: {method_count})"

def commit_snapshot(folder_path):
    snapshot_time = datetime.datetime.now()
    print(f"Snapshot taken successfully at {snapshot_time}")

def check_changes(folder_path):
    current_files = [file for file in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, file))]
    with open('.snapshot', 'r') as f:
        snapshot_time = datetime.datetime.fromisoformat(f.readline().strip())

    added_files = [file for file in current_files if os.path.getmtime(os.path.join(folder_path, file)) > snapshot_time.timestamp()]
    deleted_files = [file for file in os.listdir('.snapshot_files') if file not in current_files]

    print("Changes detected:")
    for file in added_files:
        print(f"{file} - New File")
    for file in deleted_files:
        print(f"{file} - Deleted")

def save_snapshot(folder_path):
    with open('.snapshot', 'w') as f:
        f.write(datetime.datetime.now().isoformat())
    current_files = [file for file in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, file))]
    os.makedirs('.snapshot_files', exist_ok=True)
    for file in current_files:
        os.symlink(os.path.join(folder_path, file), os.path.join('.snapshot_files', file))
    print("Snapshot saved successfully.")

def main():
    folder_path = "/path/to/your/folder"

    while True:
        action = input("Enter action (commit/check/status/exit): ")
        if action == "commit":
            commit_snapshot(folder_path)
        elif action == "check":
            check_changes(folder_path)
        elif action == "status":
            for file in os.listdir('.snapshot_files'):
                file_info = FileInfo(os.path.join('.snapshot_files', file))
                print(file_info.get_info())
        elif action == "exit":
            break
        else:
            print("Invalid action. Please try again.")

if __name__ == "__main__":
    main()

