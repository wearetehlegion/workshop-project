from telegram import ReplyKeyboardMarkup, KeyboardButton

def get_cancel_keyboard():
    keyboard = [
        [KeyboardButton("❌ Отмена")]
    ]
    return ReplyKeyboardMarkup(keyboard, resize_keyboard=True, one_time_keyboard=True)