import os
import requests

TOKEN = os.getenv("TELEGRAM_TOKEN")
CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")
STATUS_FILE = "last_status.txt"

def send_telegram_msg(text):
    if not TOKEN or not CHAT_ID: return
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    try:
        requests.get(url, params={"chat_id": CHAT_ID, "text": text}, timeout=10)
    except: pass

def get_last_status():
    if os.path.exists(STATUS_FILE):
        with open(STATUS_FILE, "r") as f:
            return f.read().strip()
    return "unknown"

def save_status(status):
    with open(STATUS_FILE, "w") as f:
        f.write(status)

def test_website_status():
    url = "https://homarr.maks-nuc.pp.ua/"
    last_status = get_last_status()
    current_status = "offline"
    
    try:
        response = requests.get(url, timeout=15)
        if response.status_code == 200:
            current_status = "online"
    except:
        current_status = "offline"

    # ЛОГІКА: Пишемо тільки якщо статус ЗМІНИВСЯ
    if current_status != last_status:
        if current_status == "online":
            send_telegram_msg("✅ Homarr знову в мережі!")
        else:
            send_telegram_msg("🚨 Homarr впав або вимкнули світло!")
        save_status(current_status)
    else:
        print(f"Статус не змінився ({current_status}). Повідомлення не надсилаємо.")

if __name__ == "__main__":
    test_website_status()
