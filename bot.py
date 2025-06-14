import logging
from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage

API_TOKEN = "YOUR_BOT_TOKEN_HERE"

# Set up bot and dispatcher
logging.basicConfig(level=logging.INFO)
bot = Bot(token=API_TOKEN)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)

# Reply keyboard setup, using 2.x style
def get_main_keyboard():
    kb = types.ReplyKeyboardMarkup(resize_keyboard=True)
    kb.add(types.KeyboardButton("Start"))
    kb.add(types.KeyboardButton("Help"))
    return kb

@dp.message_handler(commands=['start'])
async def cmd_start(message: types.Message):
    await message.reply("Welcome! Here’s your main keyboard:", reply_markup=get_main_keyboard())

@dp.message_handler(commands=['help'])
async def cmd_help(message: types.Message):
    await message.reply("Type 'Start' to begin using the bot.")

@dp.message_handler(lambda msg: msg.text == "Start")
async def handle_start_text(message: types.Message):
    await message.reply("Let’s get going! 🚀")

@dp.message_handler(lambda msg: msg.text == "Help")
async def handle_help_text(message: types.Message):
    await message.reply("How can I assist you today?")

@dp.message_handler()
async def echo_all(message: types.Message):
    await message.reply(f"You said: {message.text}")

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
