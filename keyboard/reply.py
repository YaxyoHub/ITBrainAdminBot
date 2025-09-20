from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton

def main_menu():
    return ReplyKeyboardMarkup(keyboard=[
        [KeyboardButton(text="➕ Kirim"), KeyboardButton(text="➖ Chiqim")],
        [KeyboardButton(text="📊 Statistika"), KeyboardButton(text="⬅️ Asosiy menyuga qaytish")],
    ], resize_keyboard=True)

def back_to_menu():
    return ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text="🔙 Menuga qaytish")]], resize_keyboard=True)

def statistika_menu():
    return ReplyKeyboardMarkup(keyboard=[
        [KeyboardButton(text="📈 Kirim hisoboti"), KeyboardButton(text="📉 Chiqim hisoboti")],
        [KeyboardButton(text="🔙 Menuga qaytish")]
    ], resize_keyboard=True)

def clear_back():
    return ReplyKeyboardMarkup(keyboard=[
        [KeyboardButton(text="🗑️ Tarixni tozalash")],
        [KeyboardButton(text="🔙 Ortga")]
    ], resize_keyboard=True)