import os
import requests

TOKEN = os.getenv("TELEGRAM_TOKEN")
CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")
GIST_TOKEN = os.getenv("GIST_TOKEN")
GIST_FILENAME = "server_status.txt"

def send_telegram_msg(text):
    if not TOKEN or not CHAT_ID: return
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    try:
        requests.get(url, params={"chat_id": CHAT_ID, "text": text}, timeout=10)
        print(f"Повідомлення надіслано: {text}")
    except Exception as e:
        print(f"Помилка відправки в ТГ: {e}")

def get_last_status():
    if not GIST_TOKEN: return "unknown"
    headers = {"Authorization": f"token {GIST_TOKEN}"}
    try:
        resp = requests.get("https://api.github.com/gists", headers=headers, timeout=10)
        for gist in resp.json():
            if GIST_FILENAME in gist['files']:
                raw_url = gist['files'][GIST_FILENAME]['raw_url']
                return requests.get(raw_url, timeout=10).text.strip()
    except Exception as e:
        print(f"Помилка читання Gist: {e}")
    return "unknown"

def save_status(status):
    if not GIST_TOKEN: return
    headers = {"Authorization": f"token {GIST_TOKEN}"}
    gist_id = None
    try:
        resp = requests.get("https://api.github.com/gists", headers=headers, timeout=10)
        for gist in resp.json():
            if GIST_FILENAME in gist['files']:
                gist_id = gist['id']
                break
        
        data = {"files": {GIST_FILENAME: {"content": status}}}
        if gist_id:
            requests.patch(f"https://api.github.com/gists/{gist_id}", headers=headers, json=data, timeout=10)
        else:
            requests.post("https://api.github.com/gists", headers=headers, json=data, timeout=10)
        print(f"Статус {status} збережено в Gist.")
    except Exception as e:
        print(f"Помилка запису в Gist: {e}")

def test_website_status():
    url = "https://homarr.maks-nuc.pp.ua/"
    last_status = get_last_status()
    print(f"Попередній статус: {last_status}")
    
    current_status = "offline"
    try:
        # Робимо запит. Якщо не відповість за 10 сек — це offline
        r = requests.get(url, timeout=10)
        if r.status_code == 200:
            current_status = "online"
        else:
            current_status = "offline"
            print(f"Сервер відповів кодом: {r.status_code}")
    except Exception as e:
        current_status = "offline"
        print(f"Сервер не відповідає: {e}")

    print(f"Поточний статус: {current_status}")

    if current_status != last_status:
        if current_status == "online":
            send_telegram_msg("✅ Homarr знову в мережі!")
        else:
            send_telegram_msg("🚨 Homarr впав або вимкнули світло!")
        save_status(current_status)
    else:
        print("Статус не змінився. Нічого не шлемо.")

if __name__ == "__main__":
    test_website_status()
