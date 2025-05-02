from telegram import InlineKeyboardButton, InlineKeyboardMarkup

def get_confirm_keyboard():
    keyboard = [
        [InlineKeyboardButton("📝 Сгенерировать историю", callback_data="generate_story")]
    ]
    return InlineKeyboardMarkup(keyboard)