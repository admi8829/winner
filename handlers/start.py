from aiogram import types, F
from aiogram.filters import Command
from utils import db
from keyboards import main_kb

async def start_command(message: types.Message, bot):
    user_id = message.from_user.id
    username = message.from_user.username or "User"
    full_name = message.from_user.full_name
    
    # 1. Referral Check (በሊንክ የመጣ ከሆነ)
    args = message.text.split()
    referrer_id = None
    if len(args) > 1 and args[1].isdigit():
        referrer_id = int(args[1])
        # ተጠቃሚው ራሱን እንዳይጋብዝ መከላከል
        if referrer_id == user_id:
            referrer_id = None

    # 2. Register/Update User in DB
    db.register_user(user_id, username, full_name, referrer_id)
    
    # 3. Check Channel Subscription (Force Join)
    # ማሳሰቢያ፡ CHANNEL_ID በ config ውስጥ መገለጽ አለበት
    CHANNEL_ID = -1003866954136 
    try:
        member = await bot.get_chat_member(chat_id=CHANNEL_ID, user_id=user_id)
        if member.status in ["left", "kicked"]:
            text = (
                "👋 ሰላም! ቦቱን ለመጠቀም መጀመሪያ ቻናላችንን ይቀላቀሉ።\n\n"
                "👋 Welcome! Please join our channel to use the bot."
            )
            # የቻናል መቀላቀያ በተን
            from aiogram.utils.keyboard import InlineKeyboardBuilder
            kb = InlineKeyboardBuilder()
            kb.row(types.InlineKeyboardButton(text="📢 Join Channel", url="https://t.me/ethiouh"))
            kb.row(types.InlineKeyboardButton(text="🔄 ተቀላቅያለሁ / I joined", callback_data="check_join"))
            await message.answer(text, reply_markup=kb.as_markup())
            return
    except Exception as e:
        print(f"Join check error: {e}")

    # 4. Show Language Options (አዲስ ተጠቃሚ ከሆነ)
    user_data = db.get_user_data(user_id)
    if not user_data.get('lang'):
        await message.answer("ቋንቋ ይምረጡ / Choose Language:", reply_markup=main_kb.get_lang_kb())
    else:
        lang = user_data.get('lang', 'am')
        is_admin = user_data.get('is_admin', False)
        welcome_text = "እንኳን በደህና መጡ! ምን ላግዝዎ?" if lang == 'am' else "Welcome! How can I help you?"
        await message.answer(welcome_text, reply_markup=main_kb.get_main_menu(lang, is_admin))

# --- Callback Handlers ---

async def set_language(callback: types.CallbackQuery):
    lang_code = callback.data.split('_')[1] # 'am' or 'en'
    user_id = callback.from_user.id
    
    db.update_user_lang(user_id, lang_code)
    
    user_data = db.get_user_data(user_id)
    is_admin = user_data.get('is_admin', False)
    
    text = "✅ ቋንቋ ተስተካክሏል!" if lang_code == 'am' else "✅ Language Updated!"
    await callback.message.edit_text(text)
    await callback.message.answer(text, reply_markup=main_kb.get_main_menu(lang_code, is_admin))
  
