import os
import logging
from aiogram import Bot, Dispatcher, types
from aiogram.types import Message
from aiogram.enums import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.utils.keyboard import ReplyKeyboardBuilder
from aiogram import Router
import asyncio

# Logging setup
logging.basicConfig(level=logging.INFO)

# Telegram Bot Token from environment variable
BOT_TOKEN = os.getenv("BOT_TOKEN")

# Create Bot and Dispatcher
bot = Bot(token=BOT_TOKEN, parse_mode=ParseMode.HTML)
dp = Dispatcher(storage=MemoryStorage())

# Router for commands
router = Router()

@router.message(commands=["start"])
async def cmd_start(message: Message):
    await message.answer("👋 Welcome to Losers Funnel Bot!\nSend /funnel <symbol> to get started.")

@router.message(lambda message: message.text.lower().startswith("/funnel"))
async def handle_funnel(message: Message):
    text = message.text.strip()
    try:
        symbol = text.split()[1].upper()
        # Stub response
        await message.answer(f"📊 Funnel logic for <b>{symbol}</b> is processing... [Simulated output]")
    except IndexError:
        await message.answer("⚠️ Usage: /funnel <symbol>")

# Bind router
dp.include_router(router)

# Entry point
async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())

