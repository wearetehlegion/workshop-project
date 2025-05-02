from telegram import Update
from telegram.ext import ContextTypes, CommandHandler
from keyboards.confirm_keyboard import get_confirm_keyboard

WELCOME_TEXT = (
    "👋 Привет! Готов к истории?"
)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        WELCOME_TEXT,
        reply_markup=get_confirm_keyboard()
    )

def register_start_handler(application):
    application.add_handler(CommandHandler("start", start))