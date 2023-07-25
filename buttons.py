from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton

# Кнопка основного меню
def main_menu():
    kb = InlineKeyboardMarkup(resize_keyboard=True, row_width=1)
    register = InlineKeyboardButton(text='Зарегистрироваться', callback_data='register')

    kb.add(register)

    return kb

# Кнопка для кнопка для выбора дисциплины игры
def disc_kb():
    kb = InlineKeyboardMarkup(resize_keyboard=True, row_width=2)
    button1 = InlineKeyboardButton('Counter Strike', callback_data='CS:GO')
    button2 = InlineKeyboardButton('VALORANT', callback_data='VALORANT')
    button3 = InlineKeyboardButton('DOTA 2', callback_data='DOTA 2')
    button4 = InlineKeyboardButton('FIFA', callback_data='FIFA')

    kb.add(button1, button2, button3, button4)

    return kb

def account_kb():
    kb = InlineKeyboardMarkup(resize_keyboard=True, row_width=1)
    profile = InlineKeyboardButton(text='Профиль', callback_data='profile')

    kb.add(profile)

    return kb

def phone_number_kb():
    kb = ReplyKeyboardMarkup(resize_keyboard=True)

    number = KeyboardButton('Поделиться контактом', request_contact=True)

    kb.add(number)

    return kb


