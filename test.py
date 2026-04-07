import os
import requests

# 1. Отримуємо секрети з налаштувань GitHub (Settings -> Secrets)
TOKEN = os.getenv("TELEGRAM_TOKEN")
CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")
STATUS_FILE = "last_status.txt"

def send_telegram_msg(text):
    """Відправка повідомлення в Telegram бот"""
    if not TOKEN or not CHAT_ID:
        print("⚠️ Помилка: Секрети TELEGRAM_TOKEN або TELEGRAM_CHAT_ID не знайдені!")
        return
    
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    params = {"chat_id": CHAT_ID, "text": text}
    
    try:
        requests.get(url, params=params, timeout=10)
    except Exception as e:
        print(f"Помилка відправки в Telegram: {e}")

def get_last_status():
    """Читаємо останній збережений статус із файлу"""
    if os.path.exists(STATUS_FILE):
        with open(STATUS_FILE, "r") as f:
            return f.read().strip()
    return "unknown"

def save_status(status):
    """Зберігаємо поточний статус у файл для наступної перевірки"""
    with open(STATUS_FILE, "w") as f:
        f.write(status)

def test_website_status():
    # Твій сервер Homarr на NUC
    url = "https://homarr.maks-nuc.pp.ua/"
    
    last_status = get_last_status()
    current_status = "offline"
    
    print(f"Перевіряю статус сайту: {url}...")
    
    try:
        # Чекаємо відповіді 15 секунд
        response = requests.get(url, timeout=15)
        
        if response.status_code == 200:
            current_status = "online"
            print("Сайт доступний (200 OK)")
        else:
            current_status = "offline"
            print(f"Сайт повернув помилку: {response.status_code}")
            
    except Exception as e:
        current_status = "offline"
        print(f"Сервер не відповідає (таймаут або помилка з'єднання): {e}")

    # --- ГОЛОВНА ЛОГІКА СПОВІЩЕНЬ ---
    if current_status != last_status:
        if current_status == "online":
            msg = "✅ Homarr знову в мережі! Все працює."
            print(f"Надсилаю: {msg}")
            send_telegram_msg(msg)
        else:
            msg = "🚨 Homarr впав або вимкнули світло! Сервер не доступний."
            print(f"Надсилаю: {msg}")
            send_telegram_msg(msg)
        
        # Оновлюємо збережений статус
        save_status(current_status)
    else:
        print(f"Статус не змінився ({current_status}). Повідомлення не потрібне.")

if __name__ == "__main__":
    test_website_status()
