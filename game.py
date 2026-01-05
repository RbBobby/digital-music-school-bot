import random
import re
from telebot import TeleBot
from telebot.types import ReplyKeyboardRemove
from load import load_json
import keyboard
from constants import FilePaths, SECTIONS

questions = []  # Загружаем вопросы
size_questions = 0
user_states = {}  # Состояния пользователей
random_unique_array = {}
count_of_question = 0

def converter_file_path(section: str) -> str:
    """
    Конвертирует выбранный раздел в путь к файлу с вопросами.
    """
    if section == "Нотная грамота":
        return FilePaths.MUSICAL_NOTATION_FILE
    elif section == "Квиз по терминам":
        return FilePaths.QUIZ_ON_TERMS_FILE
    elif section == "Слуховой анализ":
        return FilePaths.AUDITORY_ANALYSIS_FILE
    elif section == "Интонационные упражнения":
        return FilePaths.INTONATION_EXERCISES_FILE
    else:
        raise ValueError("Неизвестный раздел игры.")

def escape_markdown(text: str) -> str:
    """
    Экранирует специальные символы для MarkdownV2.
    """
    escape_chars = r'_*[]()~`>#+-=|{}.!'
    return re.sub(rf"([{re.escape(escape_chars)}])", r"\\\1", text)



def select_level(bot: TeleBot, message) -> None:
    """
    Показывает пользователю выбор уровня сложности викторины.
    """
    bot.send_message(
        message.chat.id,
        "Выберите уровень:",
        reply_markup=keyboard.get_levels_keyboard()
    )

def select_section(bot: TeleBot, message) -> None:
    """
    Показывает пользователю выбор раздела викторины.
    """
    bot.send_message(
        message.chat.id,
        "Выберите раздел:",
        reply_markup=keyboard.get_section_keyboard()
    )    

def start_game(bot: TeleBot, message, count = 10) -> None:
    """
    Начинает викторину с заданным количеством вопросов.
    """
    global random_unique_array, count_of_question, questions, size_questions
    questions = load_json(converter_file_path(message.text))
    user_id = message.chat.id
    size_questions = len(questions)
    count_of_question = count
    if message.text == SECTIONS["INTONATION_EXERCISES"]:
        start_intonation_exercises(bot, user_id)
        return
    # Удаляем клавиатуру и приветствуем пользователя
    bot.send_message(user_id, "Начинаем викторину!", reply_markup=ReplyKeyboardRemove())

    # Устанавливаем начальное состояние пользователя
    user_states[user_id] = {"current_question": 0, "score": 0}
    random_unique_array = random.sample(range(size_questions), size_questions)

    send_question(bot, user_id)


def send_question(bot: TeleBot, chat_id: int) -> None:
    """
    Отправляет текущий вопрос пользователю.
    Поддерживает вопросы с картинкой, видео или без медиа.
    """
    state = user_states.get(chat_id)
    if not state:
        bot.send_message(chat_id, "Ошибка: состояние пользователя не найдено.")
        return

    if state["current_question"] < count_of_question:
        question_index = random_unique_array[state["current_question"]]
        question_data = questions[question_index]

        question_text = (
            f"Вопрос №{state['current_question'] + 1} из {count_of_question}.\n\n"
            f"{question_data['question']}\n"
        )
        options_text = "\n".join(
            [f"{i + 1}) {option}" for i, option in enumerate(question_data["options"])]
        )

        # 1️⃣ Вопрос с картинкой
        if "image" in question_data and question_data["image"]:
            photo_path = f"static/musical_notation/{question_data['image']}"
            with open(photo_path, "rb") as photo:
                bot.send_photo(
                    chat_id,
                    photo,
                    caption=f"<b>{question_text}</b>\n{options_text}",
                    parse_mode="HTML",
                    reply_markup=keyboard.get_quiz_keyboard()
                )

        # 2️⃣ Вопрос с видео (mp4/mov)
        elif "media" in question_data and question_data["media"]:
            media_path = f"static/auditory_analysis/{question_data['media']}"
            with open(media_path, "rb") as video_file:
                bot.send_video(
                    chat_id,
                    video_file,
                    caption=f"<b>{question_text}</b>\n{options_text}",
                    parse_mode="HTML",
                    reply_markup=keyboard.get_quiz_keyboard()
                )

        # 3️⃣ Обычный текстовый вопрос
        else:
            bot.send_message(
                chat_id,
                f"<b>{question_text}</b>{options_text}",
                parse_mode="HTML",
                reply_markup=keyboard.get_quiz_keyboard()
            )
    else:
        close_game(bot, chat_id)
        user_states.pop(chat_id, None)  # Удаляем состояние пользователя



def close_game(bot: TeleBot, chat_id: int) -> None:
    """
    Завершает викторину и отправляет результат.
    """
    state = user_states.get(chat_id)
    if not state:
        bot.send_message(
        chat_id,
        reply_markup=keyboard.get_common_keyboard()
    )
        return

    bot.send_message(
        chat_id,
        f"Викторина завершена! Ваш результат: {state['score']} из {count_of_question}.",
        reply_markup=keyboard.get_common_keyboard()
    )

def handle_answer(bot: TeleBot, message) -> None:
    """
    Обрабатывает ответ пользователя и переходит к следующему вопросу.
    """
    state = user_states.get(message.chat.id)
    if not state:
        bot.send_message(message.chat.id, "Ошибка: состояние пользователя не найдено.")
        return

    question_index = random_unique_array[state["current_question"]]
    question_data = questions[question_index]

    if int(message.text) - 1 == question_data["correctOption"]:
        state["score"] += 1
        bot.send_message(message.chat.id, "✅ Правильно!")
    else:
        correct_option = question_data["options"][question_data["correctOption"]]
        bot.send_message(message.chat.id, f"❌ Неправильно. Правильный ответ: {correct_option}")

    state["current_question"] += 1
    send_question(bot, message.chat.id)

def start_intonation_exercises(bot: TeleBot, user_id: int) -> None:
    """
    Запускает раздел 'Интонационные упражнения'.
    Отправляет клавиатуру с номерами упражнений.
    """
    bot.send_message(
        user_id,
        "Выберите номер упражнения:",
        reply_markup=keyboard.get_key_music_keyboard()  # Клавиатура с кнопками 1–10
    )

def handle_intonation_choice(bot: TeleBot, message) -> None:
    """
    Обрабатывает выбор номера упражнения пользователем.
    Отправляет соответствующую картинку и аудиофайл.
    """
    user_id = message.chat.id

    try:
        choice = int(message.text.replace("№", "")) - 1  # Номер упражнения от 1–10
        if 0 <= choice < len(questions):
            exercise = questions[choice]

            # Отправка картинки
            with open(f"static/Intonation_exercises/{exercise['image']}", "rb") as photo:
                bot.send_photo(user_id, photo)

            # Отправка аудио
            with open(f"static/Intonation_exercises/{exercise['music']}", "rb") as music:
                bot.send_audio(user_id, music)

        else:
            bot.send_message(user_id, "Неверный номер упражнения. Выберите от 1 до 10.")
    except ValueError:
        bot.send_message(user_id, "Пожалуйста, выберите число от 1 до 10.")