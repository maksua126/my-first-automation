import os
import requests

# Тепер скрипт бере дані з секретів GitHub
TOKEN = os.getenv("TELEGRAM_TOKEN")
CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

def send_telegram_msg(text):
    if not TOKEN or not CHAT_ID:
        print("Помилка: Токен або ID не знайдені в системних змінних!")
        return
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    params = {"chat_id": CHAT_ID, "text": text}
    requests.get(url, params=params)

# ... далі твій код тесту ...
import requests  # Бібліотека для запитів до сайтів

def test_website_status():
    url = "https://www.google.com"

    print(f"Перевіряю статус сайту: {url}...")

    try:
        # Робимо запит до сайту
        response = requests.get(url)

        # Головна частина тесту: перевіряємо, чи статус-код дорівнює 200 (ОК)
        # Якщо код не 200, скрипт зупиниться з помилкою
        assert response.status_code == 200

        print("✅ Тест пройдено успішно! Сайт працює.")
        print(f"Час відповіді сервера: {response.elapsed.total_seconds()} сек.")

    except Exception as e:
        print(f"❌ Тест провалено! Щось пішло не так: {e}")

if __name__ == "__main__":
    test_website_status()

