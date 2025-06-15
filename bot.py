from aiogram import Bot, Dispatcher, F, Router
from aiogram.types import Update, Message
from aiogram.fsm.storage.memory import MemoryStorage
from fastapi import FastAPI, Request
import uvicorn
import os
import random
import logging

# Logging setup
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Telegram bot token and webhook config
TOKEN = os.getenv("BOT_TOKEN")
WEBHOOK_PATH = f"/webhook/{TOKEN}"
WEBHOOK_URL = f"https://funnel-bot-service.onrender.com{WEBHOOK_PATH}"

# Bot and Dispatcher setup
bot = Bot(token=TOKEN)
dp = Dispatcher(storage=MemoryStorage())

# Router setup
router = Router()

# /start
@router.message(F.text == "/start")
async def start_handler(message: Message):
    logger.info(f"/start triggered by {message.from_user.id}")
    await message.answer("👋 Hello! Funnel bot is live and webhook-connected.")

# /ping (debug check)
@router.message(F.text == "/ping")
async def ping_handler(message: Message):
    logger.info(f"/ping triggered by {message.from_user.id}")
    await message.answer("✅ Pong! Bot is working.")

# /funnel <stock>
@router.message(F.text.startswith("/funnel"))
async def funnel_handler(message: Message):
    parts = message.text.strip().split()
    if len(parts) != 2:
        await message.answer("⚠️ Usage: /funnel RELIANCE")
        return

    stock = parts[1].upper()
    price = random.randint(200, 1000)
    entry = price
    stop = entry - 25
    target = entry + 80

    logger.info(f"/funnel triggered for {stock} by {message.from_user.id}")

    await message.answer(
       f"📊 Funnel Projection for *{stock}*\nEntry: ₹{entry} | Stop: ₹{stop} | Target: ₹{target}",
        parse_mode="Markdown"
    )

# Sector map for scan
SECTOR_MAP = {
    "nifty 50": ["RELIANCE", "INFY", "TCS", "HDFCBANK", "SBIN", "ITC"],
    "ev": ["TATAMOTORS", "AMARAJABAT", "GREAVES"],
    "pharma": ["SUNPHARMA", "CIPLA", "DRREDDY"],
    "banking": ["HDFCBANK", "ICICIBANK", "KOTAKBANK", "AXISBANK"],
    "fmcg": ["HINDUNILVR", "DABUR", "BRITANNIA"],
    "defense": ["HAL", "BEL", "BDL", "BEML"],
    "petrochemical": ["RELIANCE", "ONGC", "GAIL"],
}

THEME_ALIASES = {
    "nifty": "nifty 50",
    "ev stocks": "ev",
    "psu banks": "banking",
    "psu": "banking",
    "fmcg sector": "fmcg",
    "defence": "defense",
}

# /scan <theme>
@router.message(F.text.startswith("/scan"))
async def scan_handler(message: Message):
    query = message.text.replace("/scan", "").strip().lower()
    theme = THEME_ALIASES.get(query, query)
    stock_list = SECTOR_MAP.get(theme)

    if not stock_list:
        await message.answer(f"⚠️ No matching theme found for: {query}")
        return

    logger.info(f"/scan triggered for theme '{theme}' by {message.from_user.id}")

    response_lines = [f"📊 Funnel Scan — *{theme.title()}*"]
    for stock in stock_list[:5]:
        rsi = random.randint(45, 75)
        vol_spike = random.choice(["✅", "⚠️", "—"])
        signal = random.choice(["Breakout", "Coil", "Watch", "Build-Up"])
        entry = random.randint(100, 1000)
        stop = entry - random.randint(10, 30)
        target = entry + random.randint(30, 80)
        response_lines.append(
            f"*{stock}* — {signal}\nEntry: ₹{entry} | Stop: ₹{stop} | Target: ₹{target}\nRSI: {rsi} | Vol Spike: {vol_spike}"
        )

    await message.answer("\n\n".join(response_lines), parse_mode="Markdown")

# /price <stock>
@router.message(F.text.startswith("/price"))
async def price_handler(message: Message):
    parts = message.text.strip().split()
    if len(parts) != 2:
        await message.answer("⚠️ Usage: /price RELIANCE")
        return

    stock = parts[1].upper()
    price = round(random.uniform(150, 3500), 2)
    ohlc = {
        "open": round(price - random.uniform(5, 20), 2),
        "high": round(price + random.uniform(5, 30), 2),
        "low": round(price - random.uniform(10, 25), 2),
        "close": round(price - random.uniform(3, 15), 2),
    }
    volume = random.randint(100000, 8000000)

    logger.info(f"/price triggered for {stock} by {message.from_user.id}")

    msg = (
        f"📉 *{stock}* — Intraday Snapshot\n"
        f"Price: ₹{price}\n"
        f"Open: ₹{ohlc['open']} | High: ₹{ohlc['high']} | Low: ₹{ohlc['low']} | Prev Close: ₹{ohlc['close']}\n"
        f"🔄 Volume: {volume:,}"
    )

    await message.answer(msg, parse_mode="Markdown")

# Register router
dp.include_router(router)

# FastAPI + Webhook
app = FastAPI()

@app.post(WEBHOOK_PATH)
async def webhook(request: Request):
    data = await request.json()
    update = Update.model_validate(data)
    await dp.feed_update(bot, update)
    return {"ok": True}

@app.on_event("startup")
async def on_startup():
    logger.info("Setting webhook...")
    await bot.set_webhook(WEBHOOK_URL)

@app.on_event("shutdown")
async def on_shutdown():
    logger.info("Removing webhook...")
    await bot.delete_webhook()

if __name__ == "__main__":
    logger.info("Starting Uvicorn server...")
    uvicorn.run("bot:app", host="0.0.0.0", port=int(os.getenv("PORT", 8000)))
