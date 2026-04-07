import os
import requests
import json

TOKEN = os.getenv("TELEGRAM_TOKEN")
CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")
GIST_TOKEN = os.getenv("GIST_TOKEN")
# Це просто назва файлу в хмарі
GIST_FILENAME = "server_status.txt"

def send_telegram_msg(text):
    if not TOKEN or not CHAT_ID: return
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    requests.get(url, params={"chat_id": CHAT_ID, "text": text}, timeout=10)

def get_last_status():
    """Отримуємо статус із GitHub Gist"""
    if not GIST_TOKEN: return "unknown"
    headers = {"Authorization": f"token {GIST_TOKEN}"}
    try:
        # Шукаємо існуючий gist з назвою server_status.txt
        response = requests.get("https://api.github.com/gists", headers=headers)
        for gist in response.json():
            if GIST_FILENAME in gist['files']:
                content_url = gist['files'][GIST_FILENAME]['raw_url']
                return requests.get(content_url).text.strip()
    except: pass
    return "unknown"

def save_status(status):
    """Зберігаємо статус у GitHub Gist"""
    if not GIST_TOKEN: return
    headers = {"Authorization": f"token {GIST_TOKEN}"}
    
    # Шукаємо чи є вже такий gist
    gist_id = None
    try:
        response = requests.get("https://api.github.com/gists", headers=headers)
        for gist in response.json():
            if GIST_FILENAME in gist['files']:
                gist_id = gist['id']
                break
    except: pass

    data = {"files": {GIST_FILENAME: {"content": status}}}
    if gist_id:
        requests.patch(f"https://api.github.com/gists/{gist_id}", headers=headers, json=data)
    else:
        requests.post("https://api.github.com/gists", headers=headers, json=data)

def test_website_status():
    url = "https://homarr.maks-nuc.pp.ua/"
    last_status = get_last_status()
    current_status = "offline"
    
    try:
        response = requests.get(url, timeout=15)
        current_status = "online" if response.status_code == 200 else "offline"
    except:
        current_status = "offline"

    print(f"Зараз: {current_status}, Було: {last_status}")

    if current_status != last_status:
        if current_status == "online":
            send_telegram_msg("✅ Homarr знову в мережі!")
        else:
            send_telegram_msg("🚨 Homarr впав або вимкнули світло!")
        save_status(current_status)

if __name__ == "__main__":
    test_website_status()
