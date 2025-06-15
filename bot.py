import os
from aiogram import Bot, Dispatcher, executor, types

# Read token from Render environment variable
BOT_TOKEN = os.getenv("BOT_TOKEN")
if not BOT_TOKEN:
    raise RuntimeError("🚨 BOT_TOKEN not found in environment!")

# Initialize bot and dispatcher
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(bot)

# Sample start command
@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    await message.reply("Hello! 🤖 Your bot is alive and ready!")

# Optional: echo handler
@dp.message_handler()
async def echo(message: types.Message):
    await message.reply(message.text)

# Run bot
if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
