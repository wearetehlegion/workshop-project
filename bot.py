import logging
import os
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from telegram import Update
from telegram.ext import Application
from register_handlers import register_all_handlers
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
DOMAIN = os.getenv("DOMAIN")

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)

app = FastAPI()

application = Application.builder().token(TOKEN).build()
register_all_handlers(application)

class UpdateDto(BaseModel):
    update_id: int
    message: dict = None
    edited_message: dict = None
    channel_post: dict = None
    edited_channel_post: dict = None
    inline_query: dict = None
    chosen_inline_result: dict = None
    callback_query: dict = None
    shipping_query: dict = None
    pre_checkout_query: dict = None
    poll: dict = None
    poll_answer: dict = None
    my_chat_member: dict = None
    chat_member: dict = None
    chat_join_request: dict = None

@app.post("/webhook/{token}")
async def telegram_webhook(token: str, update: UpdateDto):
    if token != TOKEN:
        raise HTTPException(status_code=403)
    await application.process_update(Update.de_json(update.dict(), application.bot))
    return {"ok": True}

@app.on_event("startup")
async def on_startup():
    if DOMAIN is None:
        raise RuntimeError("DOMAIN environment variable is not set")
    await application.initialize()
    webhook_url = f"{DOMAIN}/webhook/{TOKEN}"
    await application.bot.set_webhook(url=webhook_url)

@app.on_event("shutdown")
async def on_shutdown():
    await application.shutdown()