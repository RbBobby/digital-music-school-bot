import time
from telebot import TeleBot
import game
import keyboard
from constants import LEVELS, SECTIONS, MUSIC_KEYBOARDS_BUTTONS, USERS_FILE, API_TOKEN
from load import load_json, save_users


user_profiles = load_json(USERS_FILE)
user_registration_state = {}

bot = TeleBot(API_TOKEN)

@bot.message_handler(commands=['start'])
def start_command(message):
    user_id = str(message.chat.id)

    if user_id in user_profiles:
        name = user_profiles[user_id]["name"]
        bot.send_message(
            message.chat.id,
            f"С возвращением, {name}! 🎶\n"
            "Добро пожаловать в «Цифровую музыкальную школу»",
            reply_markup=keyboard.get_common_keyboard()
        )
        return

    user_registration_state[user_id] = "waiting_name"
    bot.send_message(
        message.chat.id,
        "Привет! 👋\n"
        "Добро пожаловать в «Цифровую музыкальную школу» 🎼\n\n"
        "Давай познакомимся 😊\n"
        "Напиши, пожалуйста, *имя и фамилию*.",
        parse_mode="Markdown"
    )


@bot.message_handler(func=lambda message: str(message.chat.id) in user_registration_state)
def handle_user_registration(message):
    user_id = str(message.chat.id)
    state = user_registration_state[user_id]

    # Имя и фамилия
    if state == "waiting_name":
        user_profiles[user_id] = {
            "name": message.text.strip()
        }
        user_registration_state[user_id] = "waiting_class"

        bot.send_message(
            message.chat.id,
            "Отлично! 😊\n"
            "Теперь напиши *класс* (например: 5А, 7Б).",
            parse_mode="Markdown"
        )

    # Класс
    elif state == "waiting_class":
        user_profiles[user_id]["class"] = message.text.strip()
        user_registration_state.pop(user_id)

        save_users(user_profiles, USERS_FILE)  # 💾 СОХРАНЯЕМ В JSON

        bot.send_message(
            message.chat.id,
            f"Спасибо за знакомство, {user_profiles[user_id]['name']}! 🎉\n"
            f"Класс: {user_profiles[user_id]['class']}\n\n"
            "Можем начинать обучение 🎶",
            reply_markup=keyboard.get_common_keyboard()
        )

@bot.message_handler(func=lambda message: message.text == "Начать")
def set_mode(message):
    """Выбор режима викторины."""
    game.select_level(bot, message)

@bot.message_handler(func=lambda message: message.text in LEVELS.values())
def set_level_selection(message):
    """Выбор уровня"""
    game.select_section(bot, message)


@bot.message_handler(func=lambda message: message.text in SECTIONS.values())
def set_section_selection(message):
    """Выбор раздела"""
    try:
        game.start_game(bot, message)
    except ValueError:
        bot.send_message(message.chat.id, "Ошибка в выборе количества вопросов. Попробуйте ещё раз.")

@bot.message_handler(func=lambda message: message.text in LEVELS.values())
def start_game(message):
    """Запуск игры с выбранным количеством вопросов."""
    try:
        question_count = int(message.text.split()[0])
        game.start_game(bot, message, question_count)
    except ValueError:
        bot.send_message(message.chat.id, "Ошибка в выборе количества вопросов. Попробуйте ещё раз.")

@bot.message_handler(func=lambda message: message.text in {"1", "2", "3", "4"})
def handle_answer(message):
    """Обработка ответов пользователя."""
    game.handle_answer(bot, message)

@bot.message_handler(func=lambda message: message.text in MUSIC_KEYBOARDS_BUTTONS)
def handle_intonation_choice(message):
    """Обработка ответов пользователя."""
    game.handle_intonation_choice(bot, message)    

@bot.message_handler(func=lambda message: message.text == "❌Завершить")
def close_game(message):
    """Завершение текущей викторины."""
    try:
        game.close_game(bot, message.chat.id)
    except Exception as e:
        bot.send_message(message.chat.id, "Ошибка завершения игры. Выберите опцию:", reply_markup=keyboard.get_common_keyboard())
        print(f"Ошибка завершения игры: {e}")

# Бесконечный цикл опроса
while True:
    try:
        bot.polling()
    except Exception as e:
        print(f"Критическая ошибка: {e}. Перезапуск через 5 секунд...")
        time.sleep(5)
