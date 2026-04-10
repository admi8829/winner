import os
import sys
from fastapi import FastAPI, Request
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command

# 1. የፋይል መንገድ ማስተካከያ (ለ Vercel ወሳኝ ነው)
# ይህ መስመር Python ከ 'api' ፎልደር ውጭ ያሉትን handlers, utils እና keyboards እንዲያይ ይረዳዋል
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# 2. ከሌሎች ፋይሎች አስፈላጊ የሆኑ ተግባራትን Import ማድረግ
from handlers.start import start_command, set_language
# ማሳሰቢያ፡ ሌሎች handlers (wallet, lottery) ስንሰራ እዚህ ጋር import ይደረጋሉ

# 3. Initialization
TOKEN = os.getenv("BOT_TOKEN")
WEBHOOK_URL = os.getenv("WEBHOOK_URL") # በ Vercel የሚሰጥህ URL (https://...app)
bot = Bot(token=TOKEN)
dp = Dispatcher()

# 4. Handlers Registration
# የ /start ትዕዛዝን መመዝገብ
dp.message.register(lambda m: start_command(m, bot), Command("start"))

# የቋንቋ ምርጫ (Callback) መመዝገብ
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
        update = types.Update.model_validate(update_data, context={"bot": bot})
        await dp.feed_update(bot, update)
        return {"status": "ok"}
    except Exception as e:
        print(f"Webhook Error: {e}")
        return {"status": "error", "message": str(e)}

# 6. Webhook Setup on Startup
@app.on_event("startup")
async def on_startup():
    # WEBHOOK_URL መጨረሻው ላይ / ስላለው ጥንቃቄ አድርግ
    webhook_full_url = f"{WEBHOOK_URL}{WEBHOOK_PATH}"
    await bot.set_webhook(url=webhook_full_url)

