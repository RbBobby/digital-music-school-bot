import json
import os

def load_json(file_path):
    if os.path.exists(file_path):
        with open(file_path, 'r', encoding='utf-8') as file:
            return json.load(file)
    print ("Файл не найден.")    
    return {}

def save_users(users: dict, file_path) -> None:
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(users, f, ensure_ascii=False, indent=4)