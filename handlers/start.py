from aiogram import types
from utils import db
from keyboards import main_kb

async def start_command(message: types.Message, bot):
    user_id = message.from_user.id
    username = message.from_user.username or "User"
    full_name = message.from_user.full_name
    
    # 1. መመዝገብ (ቀላል እንዲሆን መጀመሪያ እናደርገዋለን)
    db.register_user(user_id, username, full_name)
    
    # 2. ለጊዜው የቻናል ፍተሻውን እናጥፋው (Error እንዳይፈጥር)
    # በኋላ ላይ ቻናሉን በትክክል ካስተካከልን በኋላ መልሰን እናበራዋለን
    
    # 3. ቋንቋ እንዲመርጥ ማድረግ
    user_data = db.get_user_data(user_id)
    if not user_data.get('lang'):
        await message.answer("ቋንቋ ይምረጡ / Choose Language:", reply_markup=main_kb.get_lang_kb())
    else:
        lang = user_data.get('lang', 'am')
        is_admin = user_data.get('is_admin', False)
        welcome_text = "እንኳን በደህና መጡ! ምን ላግዝዎ?" if lang == 'am' else "Welcome! How can I help you?"
        await message.answer(welcome_text, reply_markup=main_kb.get_main_menu(lang, is_admin))
        
