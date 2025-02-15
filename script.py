import requests

def send_message():
    token = "${{ secrets.TELEGRAM_TOKEN }}"
    chat_id = "${{ secrets.TELEGRAM_CHANNEL_ID }}"
    message = "Привет! Этот скрипт отправлен через GitHub Actions."

    url = f"https://api.telegram.org/bot{token}/sendMessage"
    data = {"chat_id": chat_id, "text": message}
    requests.post(url, data=data)

if __name__ == "__main__":
    send_message()
