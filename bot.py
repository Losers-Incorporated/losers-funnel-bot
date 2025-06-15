from aiogram import Bot, Dispatcher, F, Router
from aiogram.types import Update, Message
from aiogram.fsm.storage.memory import MemoryStorage
from fastapi import FastAPI, Request
import uvicorn
import os

# Telegram bot token and webhook config
TOKEN = os.getenv("BOT_TOKEN")
WEBHOOK_PATH = f"/webhook/{TOKEN}"
WEBHOOK_URL = f"https://funnel-bot-service.onrender.com{WEBHOOK_PATH}"

# Bot and Dispatcher setup
bot = Bot(token=TOKEN)
dp = Dispatcher(storage=MemoryStorage())

# ✅ Setup router and handler
router = Router()

@router.message(F.text == "/start")
async def start_handler(message: Message):
    await message.answer("👋 Hello! Funnel bot is live and webhook-connected.")

# Register router to dispatcher
dp.include_router(router)

# FastAPI app
app = FastAPI()

@app.post(WEBHOOK_PATH)
async def webhook(request: Request):
    data = await request.json()
    update = Update.model_validate(data)
    await dp.feed_update(bot, update)
    return {"ok": True}

@app.on_event("startup")
async def on_startup():
    await bot.set_webhook(WEBHOOK_URL)

@app.on_event("shutdown")
async def on_shutdown():
    await bot.delete_webhook()

if __name__ == "__main__":
    uvicorn.run("bot:app", host="0.0.0.0", port=int(os.getenv("PORT", 8000)))
