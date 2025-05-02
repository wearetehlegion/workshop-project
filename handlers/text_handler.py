from telegram import Update
from telegram.ext import ContextTypes, MessageHandler, filters
from views.add_channel_view import send_story_view
from handlers.callback_handler import generate_story_with_gemini, get_giphy_gif

from db import db_manager
import asyncio

async def text_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if context.user_data.get("awaiting_custom_topic"):
        topic = update.message.text
        # Сохраняем запрос пользователя в БД
        loop = asyncio.get_running_loop()
        await loop.run_in_executor(
            None,
            db_manager.save_user_request,
            update.effective_user.username,
            update.effective_user.id,
            topic
        )
        if len(topic.split()) > 100:
            await update.message.reply_text("✍️ До 100 слов, пожалуйста.")
            return
        story, options = await generate_story_with_gemini(topic, genre="Своя тема")
        gif_url = await get_giphy_gif(story)
        await send_story_view(update, context, story, options, gif_url)
        context.user_data["genre"] = "Своя тема"
        context.user_data["story"] = story
        context.user_data["options"] = options
        context.user_data["awaiting_custom_topic"] = False
    else:
        await update.message.reply_text("🔘 Используйте кнопки ниже.")

def register_text_handler(application):
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, text_handler))