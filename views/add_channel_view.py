from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes

async def send_story_view(update: Update, context: ContextTypes.DEFAULT_TYPE, story: str, options: list, gif_url: str):
    # Сначала отправляем гифку
    if update.callback_query:
        chat_id = update.callback_query.message.chat_id
    else:
        chat_id = update.message.chat_id
    await context.bot.send_animation(chat_id=chat_id, animation=gif_url)
    # Затем отправляем историю с вариантами
    keyboard = [
        [InlineKeyboardButton(opt, callback_data=f"story_option_{i}")]
        for i, opt in enumerate(options)
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await context.bot.send_message(chat_id=chat_id, text=story, reply_markup=reply_markup)

async def ask_custom_topic_view(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.callback_query.message.reply_text(
        "📝 Введите тему истории"
    )