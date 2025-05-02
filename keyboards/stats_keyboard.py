from telegram import InlineKeyboardButton, InlineKeyboardMarkup

def get_genre_keyboard():
    keyboard = [
        [
            InlineKeyboardButton("🧙‍♂️ Фентези", callback_data="genre_fantasy"),
            InlineKeyboardButton("🤖 Фантастика", callback_data="genre_scifi"),
        ],
        [
            InlineKeyboardButton("👻 Крипипаста", callback_data="genre_creepypasta"),
            InlineKeyboardButton("✍️ Своя тема", callback_data="genre_custom"),
        ]
    ]
    return InlineKeyboardMarkup(keyboard)