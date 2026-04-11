from aiogram import types
from utils import db
from keyboards import main_kb

async def start_command(message: types.Message, bot):
    user_id = message.from_user.id
    username = message.from_user.username or "User"
    full_name = message.from_user.full_name
    
    # ተጠቃሚውን መመዝገብ
    db.register_user(user_id, username, full_name)
    
    # ቋንቋ እንዲመርጥ ማድረግ
    user_data = db.get_user_data(user_id)
    if not user_data or not user_data.get('lang'):
        await message.answer("ቋንቋ ይምረጡ / Choose Language:", reply_markup=main_kb.get_lang_kb())
    else:
        lang = user_data.get('lang', 'am')
        is_admin = user_data.get('is_admin', False)
        welcome_text = "እንኳን በደህና መጡ! ምን ላግዝዎ?" if lang == 'am' else "Welcome! How can I help you?"
        await message.answer(welcome_text, reply_markup=main_kb.get_main_menu(lang, is_admin))

# ይህ ነው የጎደለው የነበረው ፋንክሽን
async def set_language(callback: types.CallbackQuery):
    lang_code = callback.data.split('_')[1] # 'am' or 'en'
    user_id = callback.from_user.id
    
    db.update_user_lang(user_id, lang_code)
    
    user_data = db.get_user_data(user_id)
    is_admin = user_data.get('is_admin', False)
    
    text = "✅ ቋንቋ ተስተካክሏል!" if lang_code == 'am' else "✅ Language Updated!"
    await callback.message.edit_text(text)
    await callback.message.answer(text, reply_markup=main_kb.get_main_menu(lang_code, is_admin))
        
