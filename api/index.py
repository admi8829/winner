import os
import sys
import logging
from fastapi import FastAPI, Request
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.types import Update

# Logs እንዲታይ ማድረግ
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# 1. የፋይል መንገድ ማስተካከያ
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# 2. Handlers Import
from handlers.start import start_command, set_language

# 3. Initialization
TOKEN = os.getenv("BOT_TOKEN")
WEBHOOK_URL = os.getenv("WEBHOOK_URL") 
bot = Bot(token=TOKEN)
dp = Dispatcher()

# 4. Handlers Registration
dp.message.register(lambda m: start_command(m, bot), Command("start"))
dp.callback_query.register(set_language, lambda c: c.data.startswith("set_"))

# 5. FastAPI Setup
app = FastAPI()
WEBHOOK_PATH = f"/bot/{TOKEN}"

@app.get("/")
async def root():
    return {"message": "Telegram Bot is running! 🚀"}

@app.post(WEBHOOK_PATH)
async def bot_webhook(request: Request):
    try:
        update_data = await request.json()
        logger.info(f"Received update: {update_data}") # መልእክቱ እንደደረሰ በሎግ ያሳየናል
        
        update = Update.model_validate(update_data, context={"bot": bot})
        await dp.feed_update(bot, update)
        return {"status": "ok"}
    except Exception as e:
        logger.error(f"Webhook Error: {e}")
        return {"status": "error", "message": str(e)}

@app.on_event("startup")
async def on_startup():
    # WEBHOOK_URL-ን ከ / ጋር በአግባቡ ማገናኘት
    base_url = WEBHOOK_URL.rstrip('/')
    webhook_full_url = f"{base_url}{WEBHOOK_PATH}"
    await bot.set_webhook(url=webhook_full_url)
    logger.info(f"Webhook set to: {webhook_full_url}")
        
