import os
from supabase import create_client, Client

# Supabase Setup
URL = os.getenv("SUPABASE_URL")
KEY = os.getenv("SUPABASE_KEY")
supabase: Client = create_client(URL, KEY)

# --- 1. USER MANAGEMENT ---

def register_user(user_id, username, full_name, referrer_id=None):
    """አዲስ ተጠቃሚ ይመዘግባል፣ ካለ ደግሞ መረጃውን ያድሳል"""
    data = {
        "user_id": user_id,
        "username": username,
        "full_name": full_name,
        "referred_by": referrer_id
    }
    try:
        # upsert ማለት ካለ Update ያደርጋል፣ ከሌለ Insert ያደርጋል
        supabase.table("users").upsert(data).execute()
        return True
    except Exception as e:
        print(f"DB Error (register_user): {e}")
        return False

def get_user_data(user_id):
    """የአንድን ተጠቃሚ ሙሉ መረጃ ያመጣል (Balance, Points...)"""
    res = supabase.table("users").select("*").eq("user_id", user_id).execute()
    return res.data[0] if res.data else None

def update_user_lang(user_id, lang):
    supabase.table("users").update({"lang": lang}).eq("user_id", user_id).execute()

# --- 2. WALLET & TRANSACTIONS ---

def add_deposit_request(user_id, amount, file_id):
    """ተጠቃሚው ደረሰኝ ሲልክ 'pending' ግብይት ይመዘግባል"""
    data = {
        "user_id": user_id,
        "amount": amount,
        "type": "deposit",
        "status": "pending",
        "receipt_file_id": file_id
    }
    return supabase.table("transactions").insert(data).execute()

def approve_transaction(transaction_id):
    """አድሚኑ ክፍያ ሲያጸድቅ ወደ Wallet ብር ይጨምራል"""
    # 1. የግብይቱን መረጃ አምጣ
    tx = supabase.table("transactions").select("*").eq("id", transaction_id).execute()
    if not tx.data: return False
    
    user_id = tx.data[0]['user_id']
    amount = tx.data[0]['amount']
    
    # 2. የተጠቃሚውን Balance አድስ
    user = get_user_data(user_id)
    new_balance = float(user['balance']) + float(amount)
    supabase.table("users").update({"balance": new_balance}).eq("user_id", user_id).execute()
    
    # 3. የግብይቱን Status 'approved' አድርግ
    supabase.table("transactions").update({"status": "approved"}).eq("id", transaction_id).execute()
    return True

# --- 3. LOTTERY & TICKETS ---

def buy_ticket(user_id, price, lottery_type):
    """ከትኬት መቁረጫ ብር ቀንሶ ትኬት ይሰጣል"""
    user = get_user_data(user_id)
    if float(user['balance']) < price:
        return False, "Insufficient balance"
    
    # ብር ቀንስ
    new_balance = float(user['balance']) - price
    supabase.table("users").update({"balance": new_balance}).eq("user_id", user_id).execute()
    
    # ትኬት መዝግብ
    res = supabase.table("tickets").insert({"user_id": user_id, "lottery_type": lottery_type}).execute()
    return True, res.data[0]['ticket_number']

# --- 4. ADMIN & WINNERS ---

def get_all_tickets():
    """አንተ አሸናፊ ለመምረጥ ሁሉንም ትኬቶች እንድታይ"""
    res = supabase.table("tickets").select("ticket_number, user_id").execute()
    return res.data

def register_winner(ticket_number, prize):
    """አሸናፊውን ይመዘግባል"""
    data = {"ticket_number": ticket_number, "prize_amount": prize}
    return supabase.table("winners").insert(data).execute()
  
