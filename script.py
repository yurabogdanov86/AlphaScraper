import os
import requests

def send_message():
    # Получаем секреты из переменных окружения
    token = os.getenv('TELEGRAM_TOKEN')  # Получаем Telegram токен
    chat_id = os.getenv('TELEGRAM_CHANNEL_ID')  # Получаем ID канала

    # Отладка: выводим секреты, чтобы убедиться, что они правильно загружаются
    print(f"Token: {token}")  # Это только для отладки, чтобы проверить корректность значения
    print(f"Chat ID: {chat_id}")  # Это только для отладки, чтобы проверить корректность значения
    
    if not token or not chat_id:
        print("Ошибка! Токен или ID канала не были найдены.")
        return

    message = "Привет! Этот скрипт отправлен через GitHub Actions."

    # Формируем URL для Telegram API
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    
    # Формируем данные запроса
    data = {"chat_id": chat_id, "text": message}
    
    # Отправляем запрос в Telegram
    response = requests.post(url, data=data)
    
    # Печатаем результат отправки сообщения
    if response.status_code == 200:
        print("Сообщение успешно отправлено!")
    else:
        print(f"Ошибка отправки сообщения: {response.status_code}, {response.text}")

if __name__ == "__main__":
    send_message()
