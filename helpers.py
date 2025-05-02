from telegram import Update
from telegram.ext import ContextTypes

async def send_story(update: Update, context: ContextTypes.DEFAULT_TYPE, text: str):
    """
    Отправляет длинный текст истории частями по 1000 символов через reply_text.
    """
    max_length = 1000
    for i in range(0, len(text), max_length):
        await update.message.reply_text(text[i:i+max_length])