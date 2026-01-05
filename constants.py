from dotenv import load_dotenv
import os

load_dotenv()  # Загружает .env

API_TOKEN = os.getenv("BOT_TOKEN")
# Уровни сложности
LEVELS = {
    "BEGINNER": "Начальный уровень",
    "INTERMEDIATE": "Средний уровень",
    "ADVANCED": "Тяжелый уровень"
}

# Разделы игры
SECTIONS = {
    "MUSICAL_NOTATION": "Нотная грамота",
    "TERMS_QUIZ": "Квиз по терминам",
    "AUDITORY_ANALYSIS": "Слуховой анализ",
    "INTONATION_EXERCISES": "Интонационные упражнения"
}

MUSIC_KEYBOARDS_BUTTONS = ["№1", "№2", "№3", "№4", "№5", "№6", "№7", "№8", "№9", "№10"]

class FilePaths:
    QUIZ_ON_TERMS_FILE = r"static\quiz_on_terms\quiz_on_terms_level_1.json"
    MUSICAL_NOTATION_FILE = r"static\musical_notation\musical_notation_level_1.json"
    INTONATION_EXERCISES_FILE = r"static\Intonation_exercises\Intonation_exercises_level_1.json"
    AUDITORY_ANALYSIS_FILE = r"static\auditory_analysis\auditory_analysis_level_1.json"

USERS_FILE = "storage/users.json"
