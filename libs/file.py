import os
from PIL import Image

def get_files_from_folder(folder_path: str, extensions: list[str] = None) -> list[str]:
    try:
        return [
            os.path.abspath(os.path.join(folder_path, f))
            for f in os.listdir(folder_path)
            if os.path.isfile(os.path.join(folder_path, f)) and 
               (extensions is None or os.path.splitext(f)[1].lower() in [ext.lower() for ext in extensions])
        ]
    except FileNotFoundError:
        print("The specified folder does not exist.")

        return []
    except PermissionError:
        print("You do not have permission to access this folder.")

        return []
    
def read_file(file_path: str) -> str:
    with open(file=file_path, mode='r', encoding='utf8') as f:
        return ''.join(f.readlines())

def write_file(file_path: str, content: str):
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    
    with open(file=file_path, mode='w', encoding='utf8') as f:
        f.write(content)

def write_image(file_path: str, image: Image):
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    
    image.save(file_path)