from telegram import Update, InputMediaAnimation
from telegram.ext import ContextTypes, CallbackQueryHandler, MessageHandler, filters
from keyboards.stats_keyboard import get_genre_keyboard
from views.add_channel_view import send_story_view
from views.add_channel_view import ask_custom_topic_view
import json

import os
import asyncio
import google.generativeai as genai
import aiohttp
import re

# --- Заглушки для Gemini и Giphy ---
async def generate_story_with_gemini(prompt: str, genre: str | None = None, user_choice: str | None = None):
    """
    Generates a story with Google Gemini Pro.
    """
    api_key = os.getenv("GEMINI_API_KEY")          # make sure this is set in your environment
    if not api_key:
        raise RuntimeError("Environment variable GEMINI_API_KEY is not set")

    genai.configure(api_key=api_key)
    model = genai.GenerativeModel("gemini-2.0-flash")    # ← choose the model you need

    # Формируем промпт для генерации истории на русском языке
    if user_choice is None:
        if genre is None:
            story_prompt = f"Пиши на русском языке.\n{prompt}"
        else:
            story_prompt = f"Пиши на русском языке.\nНапиши историю жанра {genre} о: {prompt}"
    else:
        if genre is None:
            story_prompt = f"Пиши на русском языке.\n{prompt}"
        else:
            story_prompt = f"Пиши на русском языке.\nНапиши историю жанра {genre} о: {prompt}"
        story_prompt += (
            "\n\nСгенерируй только продолжение истории отдельным сообщением, без повторения предыдущего текста."
        )

    # Формируем единый запрос, чтобы получить и саму историю, и варианты её продолжения
    full_prompt = (
        f"{story_prompt}\n\n"
        "Сгенерируй ответ *строго* в формате JSON:\n"
        '{\n'
        '  "story": "<текст истории>",\n'
        '  "options": ["<вариант 1>", "<вариант 2>", "<вариант 3>"]\n'
        "}\n"
        "Без дополнительного текста, только JSON."
    )

    # google-generativeai синхронный → уводим в отдельный поток
    response = await asyncio.to_thread(model.generate_content, full_prompt)

    # Пытаемся распарсить JSON; если не выйдет — вернём историю без вариантов
    try:
        raw = response.text.strip()
        if raw.startswith("```"):
            raw = raw.strip("`").lstrip("json").strip()
        data = json.loads(raw)
        story = data.get("story", "")
        options = data.get("options", [])
    except Exception:
        story = response.text
        options = []

    # --- Пост-обработка вариантов для кнопок ---
    def is_russian(text):
        return bool(re.search(r"[а-яА-ЯёЁ]", text))

    def starts_with_emoji(text):
        # Проверка на наличие эмодзи в начале строки (основные диапазоны)
        return bool(re.match(r"^[\U0001F300-\U0001FAFF\U00002600-\U000027BF]", text))

    def add_emoji(text, emoji="📖"):
        return f"{emoji} {text}"

    processed_options = []
    for opt in options:
        # Оставить только варианты на русском
        if not is_russian(opt):
            continue
        # Обрезать до 5 слов
        words = opt.strip().split()
        opt_short = " ".join(words[:5])
        # Добавить эмодзи, если нет
        if not starts_with_emoji(opt_short):
            opt_short = add_emoji(opt_short)
        processed_options.append(opt_short)

    return story, processed_options

async def get_giphy_gif(story_text):
    """
    Отправляет текст истории в Giphy Service и возвращает URL гифки.
    """
    url = "http://localhost:8000/gif"
    payload = {"text": story_text}
    try:
        async with aiohttp.ClientSession() as session:
            async with session.post(url, json=payload) as resp:
                if resp.status == 200:
                    data = await resp.json()
                    return data.get("gif_url")
                else:
                    # В случае ошибки возвращаем дефолтную гифку
                    return "https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExZ2lmLXN0dWJibGVnZW5lcmF0ZWQ/3oEjI6SIIHBdRxXI40/giphy.gif"
    except Exception:
        # В случае ошибки возвращаем дефолтную гифку
        return "https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExZ2lmLXN0dWJibGVnZW5lcmF0ZWQ/3oEjI6SIIHBdRxXI40/giphy.gif"

# --- Callback Handler ---
async def callback_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    data = query.data

    if data == "generate_story":
        await query.message.reply_text(
            "📚 Выберите жанр истории",
            reply_markup=get_genre_keyboard()
        )
    elif data.startswith("genre_"):
        genre = data.split("_")[1]
        if genre == "custom":
            await ask_custom_topic_view(update, context)
            context.user_data["awaiting_custom_topic"] = True
        else:
            story, options = await generate_story_with_gemini("", genre=genre)
            gif_url = await get_giphy_gif(story)
            await send_story_view(update, context, story, options, gif_url)
            context.user_data["genre"] = genre
            context.user_data["story"] = story
            context.user_data["options"] = options
    elif data.startswith("story_option_"):
        option_idx = int(data.split("_")[-1])
        genre = context.user_data.get("genre", "Фентези")
        prev_story = context.user_data.get("story", "")
        options = context.user_data.get("options", [])
        user_choice = options[option_idx] if option_idx < len(options) else ""
        story, new_options = await generate_story_with_gemini(prev_story, genre=genre, user_choice=user_choice)
        gif_url = await get_giphy_gif(story)
        await send_story_view(update, context, story, new_options, gif_url)
        context.user_data["story"] = story
        context.user_data["options"] = new_options

def register_callback_handler(application):
    application.add_handler(CallbackQueryHandler(callback_handler))
