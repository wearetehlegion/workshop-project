from telegram import Update
from telegram.ext import ContextTypes

async def error_handler(update: object, context: ContextTypes.DEFAULT_TYPE):
    print(f"Ошибка: {context.error}")

def register_error_handler(application):
    application.add_error_handler(error_handler)