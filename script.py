import requests

def send_message():
    token = "7229132515:AAHx9mho6IQn2LnseRtVxT_3Z6h0UfeeG6E"  # Замените на ваш токен
    chat_id = "-1002424946552"  # Замените на ваш канал
    message = "Привет! Этот скрипт отправлен через GitHub Actions."

    url = f"https://api.telegram.org/bot{token}/sendMessage"
    data = {"chat_id": chat_id, "text": message}
    requests.post(url, data=data)

if __name__ == "__main__":
    send_message()
