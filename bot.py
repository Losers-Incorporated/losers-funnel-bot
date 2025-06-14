import os
from aiogram import Bot, Dispatcher, types
from aiogram.utils import executor

# ✅ Load BOT_TOKEN from Render's environment
BOT_TOKEN = os.getenv("BOT_TOKEN")
if not BOT_TOKEN:
    raise ValueError("BOT_TOKEN is missing! Set it in your Render environment variables.")

# ✅ Initialize bot and dispatcher
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(bot)

# ✅ Basic start command
@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    await message.reply("Welcome! Your bot is running successfully 🚀")

# ✅ Basic echo fallback
@dp.message_handler()
async def echo(message: types.Message):
    await message.reply(f"You said: {message.text}")

# ✅ Launch polling
if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
