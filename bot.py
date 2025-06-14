import logging
import os
from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage

# 🔐 Get token securely from environment (Render dashboard > Environment > BOT_TOKEN)
BOT_TOKEN = os.getenv("BOT_TOKEN")

# Logging setup
logging.basicConfig(level=logging.INFO)

# Bot and dispatcher setup
bot = Bot(token=BOT_TOKEN)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)

# ✅ Reply keyboard (manual, aiogram 2 style)
def get_main_keyboard():
    kb = types.ReplyKeyboardMarkup(resize_keyboard=True)
    kb.add(types.KeyboardButton("Start"))
    kb.add(types.KeyboardButton("Help"))
    return kb

# 🟢 /start command
@dp.message_handler(commands=['start'])
async def cmd_start(message: types.Message):
    await message.reply("Welcome to the Funnel Engine Bot! 🚀", reply_markup=get_main_keyboard())

# 🟡 /help command
@dp.message_handler(commands=['help'])
async def cmd_help(message: types.Message):
    await message.reply("This bot runs Losers Inc Funnel Pattern Engine. Type 'Start' to begin.")

# Handle Start button
@dp.message_handler(lambda msg: msg.text == "Start")
async def handle_start_text(message: types.Message):
    await message.reply("Initiating full funnel scan... 🔍")

# Handle Help button
@dp.message_handler(lambda msg: msg.text == "Help")
async def handle_help_text(message: types.Message):
    await message.reply("You can ask for breakout stocks, funnel simulations, or volume alerts.")

# 🪞 Echo fallback
@dp.message_handler()
async def echo_all(message: types.Message):
    await message.reply(f"You said: {message.text}")

# Entry point
if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
