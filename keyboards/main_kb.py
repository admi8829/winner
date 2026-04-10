from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder

# 1. ዋና ሜኑ (Main Menu)
def get_main_menu(lang='am', is_admin=False):
    kb = ReplyKeyboardBuilder()
    
    if lang == 'am':
        buttons = [
            "➕ ትኬት ቁረጥ", "💰 ቦርሳ (Wallet)",
            "👤 ፕሮፋይል", "👥 ጓደኛ ጋብዝ",
            "🏆 አሸናፊዎች", "📊 መረጃ",
            "🌐 Language", "💡 እገዛ"
        ]
        if is_admin:
            buttons.append("⚙️ Admin Panel")
    else:
        buttons = [
            "➕ Buy Ticket", "💰 Wallet",
            "👤 Profile", "👥 Invite",
            "🏆 Winners", "📊 Stats",
            "🌐 Language", "💡 Help"
        ]
        if is_admin:
            buttons.append("⚙️ Admin Panel")

    for btn in buttons:
        kb.button(text=btn)
    
    kb.adjust(2, 2, 2, 2, 1) # በተኖቹ በሁለት ረድፍ እንዲደደሩ
    return kb.as_markup(resize_keyboard=True)

# 2. የWallet (የብር ማስገቢያ) ኢንላይን በተን
def get_wallet_kb(lang='am'):
    kb = InlineKeyboardBuilder()
    if lang == 'am':
        kb.button(text="💳 ብር አስገባ (Deposit)", callback_data="deposit")
        kb.button(text="💸 ብር አውጣ (Withdraw)", callback_data="withdraw")
    else:
        kb.button(text="💳 Deposit", callback_data="deposit")
        kb.button(text="💸 Withdraw", callback_data="withdraw")
    return kb.as_markup()

# 3. የክፍያ ማጽደቂያ (ለአድሚን ብቻ የሚላክ)
def get_admin_confirm_kb(tx_id):
    kb = InlineKeyboardBuilder()
    kb.button(text="✅ አጽድቅ (Approve)", callback_data=f"conf_{tx_id}")
    kb.button(text="❌ ሰርዝ (Reject)", callback_data=f"rejc_{tx_id}")
    return kb.as_markup()

# 4. የቋንቋ መምረጫ
def get_lang_kb():
    kb = InlineKeyboardBuilder()
    kb.button(text="አማርኛ 🇪🇹", callback_data="set_am")
    kb.button(text="English 🇺🇸", callback_data="set_en")
    return kb.as_markup()
          
