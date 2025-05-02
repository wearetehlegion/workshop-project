from telegram import Update
from telegram.ext import ContextTypes, CommandHandler

async def admin(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("⛔ Нет доступа к панели.")

def register_admin_handler(application):
    application.add_handler(CommandHandler("admin", admin))