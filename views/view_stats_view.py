from telegram import Update
from telegram.ext import ContextTypes
from db.db_manager import get_user_stats

async def view_stats_view(update: Update, context: ContextTypes.DEFAULT_TYPE):
    stats = get_user_stats()
    if not stats:
        await update.message.reply_text("📊 Нет статистики сейчас.")
    else:
        await update.message.reply_text(f"📊 Ваша статистика: {stats}")