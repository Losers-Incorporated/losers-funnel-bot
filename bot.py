import os
from aiogram import Bot, Dispatcher, types
from aiogram.utils import executor

BOT_TOKEN = os.getenv("BOT_TOKEN")
if not BOT_TOKEN:
    raise ValueError("🚨 BOT_TOKEN is missing! Check your Render environment variables.")

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(bot)

@dp.message_handler(commands=['start'])
async def cmd_start(message: types.Message):
    await message.reply("✅ Bot is running!")

@dp.message_handler()
async def echo(message: types.Message):
    await message.reply(f"You said: {message.text}")

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
