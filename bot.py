from aiogram import Bot, Dispatcher, F, Router
from aiogram.types import Update, Message
from aiogram.fsm.storage.memory import MemoryStorage
from fastapi import FastAPI, Request
import uvicorn
import os
import random

# Telegram bot token and webhook config
TOKEN = os.getenv("BOT_TOKEN")
WEBHOOK_PATH = f"/webhook/{TOKEN}"
WEBHOOK_URL = f"https://funnel-bot-service.onrender.com{WEBHOOK_PATH}"

bot = Bot(token=TOKEN)
dp = Dispatcher(storage=MemoryStorage())
router = Router()

# /start
@router.message(F.text == "/start")
async def start_handler(message: Message):
    await message.answer("👋 Hello! Funnel bot is live and webhook-connected.")

# /funnel <stock>
@router.message(F.text.startswith("/funnel"))
async def funnel_handler(message: Message):
    parts = message.text.strip().split()
    if len(parts) != 2:
        await message.answer("⚠️ Usage: /funnel RELIANCE")
        return
    stock = parts[1].upper()
    entry = random.randint(100, 1000)
    stop = entry - random.randint(10, 30)
    target = entry + random.randint(30, 80)
    await message.answer(
        f"📊 Funnel Projection for *{stock}*
Entry: ₹{entry} | Stop: ₹{stop} | Target: ₹{target}",
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

    header = "| Stock | Signal | Entry | Stop | Target Zone | RSI | Vol Spike | Funnel Type |
"
    header += "|-------|--------|-------|------|--------------|-----|------------|--------------|"
    rows = []
    for stock in stock_list[:5]:
        rsi = random.randint(40, 80)
        entry = random.randint(100, 1500)
        stop = entry - random.randint(10, 40)
        target1 = entry + random.randint(30, 60)
        target2 = target1 + random.randint(20, 40)
        vol_spike = random.choice(["✅ +45%", "⚠ +28%", "—"])
        signal = random.choice(["Breakout", "Build-Up", "Coil", "Retest"])
        funnel = random.choice(["Asc. Retest", "Vol Coil", "Range Play"])
        row = f"| {stock} | {signal} | ₹{entry} | ₹{stop} | ₹{target1}–₹{target2} | {rsi} | {vol_spike} | {funnel} |"
        rows.append(row)

    table = "
".join([header] + rows)
    await message.answer(f"```
{table}
```", parse_mode="Markdown")

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
        "close": round(price + random.uniform(3, 15), 2),
    }
    volume = random.randint(100000, 8000000)
    msg = (
        f"📈 *{stock}* — Intraday Snapshot\n"
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
    await bot.set_webhook(WEBHOOK_URL)

@app.on_event("shutdown")
async def on_shutdown():
    await bot.delete_webhook()

if __name__ == "__main__":
    uvicorn.run("bot:app", host="0.0.0.0", port=int(os.getenv("PORT", 8000)))
