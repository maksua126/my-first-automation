import os
import requests

# 1. Отримуємо секрети з хмари GitHub
TOKEN = os.getenv("TELEGRAM_TOKEN")
CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

def send_telegram_msg(text):
    if not TOKEN or not CHAT_ID:
        print("⚠️ Помилка: Токен або ID не знайдені в Secrets!")
        return
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    params = {"chat_id": CHAT_ID, "text": text}
    try:
        requests.get(url, params=params, timeout=10)
    except Exception as e:
        print(f"Помилка відправки в Telegram: {e}")

def test_website_status():
    # Твій сервер Homarr на NUC
    url = "https://homarr.maks-nuc.pp.ua/"
    print(f"Перевіряю статус сайту: {url}...")
    
    try:
        response = requests.get(url, timeout=15)
        
        if response.status_code == 200:
            status_text = f"✅ Homarr працює! (Відповідь: {response.elapsed.total_seconds()}с)"
            print(status_text)
            send_telegram_msg(status_text)
        else:
            error_text = f"⚠️ Homarr повернув помилку: {response.status_code}"
            print(error_text)
            send_telegram_msg(error_text)
            
    except Exception as e:
        fail_text = f"🚨 Homarr НЕ ДОСТУПНИЙ! Можливо, вимкнули світло.\nПомилка: {e}"
        print(fail_text)
        send_telegram_msg(fail_text)

if __name__ == "__main__":
    test_website_status()
