from telebot import types
from constants import LEVELS, SECTIONS

def get_common_keyboard():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn_quiz = types.KeyboardButton("Начать")

    markup.row(btn_quiz)
    return markup

def get_quiz_keyboard():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn_1 = types.KeyboardButton("1")
    btn_2 = types.KeyboardButton("2")
    btn_3 = types.KeyboardButton("3")
    btn_4 = types.KeyboardButton("4")
    btn_5 = types.KeyboardButton("❌Завершить")
    markup.row(btn_1, btn_2)
    markup.row(btn_3, btn_4)
    markup.row(btn_5)
    return markup


def get_levels_keyboard():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn_1 = types.KeyboardButton(LEVELS["BEGINNER"])
    btn_2 = types.KeyboardButton(LEVELS["INTERMEDIATE"])
    btn_3 = types.KeyboardButton(LEVELS["ADVANCED"])
    markup.row(btn_1)
    markup.row(btn_2, btn_3)
    return markup

def get_section_keyboard():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn_1 = types.KeyboardButton(SECTIONS["MUSICAL_NOTATION"])
    btn_2 = types.KeyboardButton(SECTIONS["TERMS_QUIZ"])
    btn_3 = types.KeyboardButton(SECTIONS["AUDITORY_ANALYSIS"])
    btn_4 = types.KeyboardButton(SECTIONS["INTONATION_EXERCISES"])
    markup.row(btn_1, btn_2)
    markup.row(btn_3, btn_4)
    return markup

def get_key_music_keyboard():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn_1 = types.KeyboardButton("№1")
    btn_2 = types.KeyboardButton("№2")
    btn_3 = types.KeyboardButton("№3")
    btn_4 = types.KeyboardButton("№4")
    btn_5 = types.KeyboardButton("№5")
    btn_6 = types.KeyboardButton("№6")
    btn_7 = types.KeyboardButton("№7")
    btn_8 = types.KeyboardButton("№8")
    btn_9 = types.KeyboardButton("№9")
    btn_10 = types.KeyboardButton("№10")
    btn_11 = types.KeyboardButton("❌Завершить")

    markup.row(btn_1, btn_2, btn_3, btn_4)
    markup.row(btn_5, btn_6, btn_7, btn_8)
    markup.row(btn_9, btn_10)
    markup.row(btn_11)
    return markup