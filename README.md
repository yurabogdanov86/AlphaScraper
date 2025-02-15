# AlphaScraper

Настройка GitHub Actions для автоматизации выполнения задач
________________________________________
Цель

Этот документ поможет вам настроить GitHub Actions для автоматизации выполнения задач, таких как тестирование, развертывание или выполнение скриптов. Мы создадим новый репозиторий, добавим рабочий процесс (workflow) и настроим его для ручного запуска.
________________________________________
План

1.	Создать новый репозиторий на GitHub.
2.	Заполнить информацию о репозитории и выбрать параметры видимости.
3.	Добавить основной скрипт (script.py) в репозиторий.
4.	Создать файл зависимостей requirements.txt.
5.	Создать и настроить GitHub Actions workflow.
6.	Добавить секреты (API-ключи) и запустить workflow вручную.
7.	Проверить успешное выполнение workflow и отладить возможные ошибки.
________________________________________
Шаг 1: Создание нового репозитория на GitHub
1.	Откройте GitHub и войдите в свой аккаунт.
2.	В верхнем правом углу нажмите на значок “+”.
3.	В выпадающем меню выберите “New repository”.
________________________________________
Шаг 2: Заполнение информации о репозитории
1.	Owner (Владелец) – Убедитесь, что выбран ваш аккаунт.
2.	Repository name (Имя репозитория) – Введите уникальное имя для вашего проекта.
3.	Description (Описание, необязательно) – Укажите краткое описание проекта, например:
o	"Этот репозиторий содержит код для автоматизированного сбора данных и отправки уведомлений в Telegram."
4.	Выберите видимость репозитория:
o	Public – репозиторий будет доступен всем в интернете.
o	Private – только вы и приглашённые пользователи смогут видеть репозиторий.
5.	Инициализация репозитория (опционально):
o	Add a README file – добавит файл README.md, в котором можно написать описание проекта.
o	Add .gitignore – выберите шаблон, если хотите игнорировать определённые файлы (например, для Python можно выбрать Python).
________________________________________
Шаг 3: Добавление основного скрипта (script.py) и файла зависимостей (requirements.txt) с отладкой
1.	Перейдите в ваш репозиторий на GitHub.
2.	Нажмите на вкладку Code.
3.	Нажмите на значок + справа от вкладки Code, затем выберите Create new file.
4.	В поле имени файла введите script.py.
5.	Перед добавлением основного скрипта важно убедиться, что секреты загружаются корректно. Для этого включим отладочные выводы, которые помогут проверить, правильно ли передаются значения API-токена и ID канала.
python
Копировать
import os
import requests

def send_message():
    # Получаем секреты из переменных окружения
    token = os.getenv('TELEGRAM_TOKEN')  # Получаем Telegram токен
    chat_id = os.getenv('TELEGRAM_CHANNEL_ID')  # Получаем ID канала

    # Отладка: выводим секреты, чтобы убедиться, что они правильно загружаются
    print(f"Token: {token}")  # Это только для отладки
    print(f"Chat ID: {chat_id}")  # Это только для отладки
    
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
6.	Нажмите Commit new file, чтобы сохранить файл в репозитории.
7.	Теперь создайте файл requirements.txt, который содержит список зависимостей для скрипта:
o	В поле имени файла введите requirements.txt.
o	Вставьте список необходимых библиотек, например:
txt
Копировать
requests
o	Нажмите Commit new file, чтобы сохранить файл.
8.	Теперь у вас есть оба файла: script.py и requirements.txt, которые необходимы для успешной работы вашего проекта.
________________________________________
Шаг 4: Настройка GitHub Actions
1.	Создайте папку для workflows:
o	Перейдите в ваш репозиторий на сайте GitHub.
o	Нажмите на вкладку Code.
o	Нажмите на значок + справа от вкладки Code, затем выберите Create new file.
o	В поле имени файла введите .github/workflows/manual_scraper.yml.
o	GitHub автоматически создаст необходимые папки, если их ещё нет.
2.	Создайте файл workflow:
o	В этой папке создайте файл manual_scraper.yml.
o	Откройте файл и добавьте следующий код:
yaml
Копировать
# Workflow для ручного запуска скрипта
name: Manual Scraper Run
on:
  workflow_dispatch:
jobs:
  run-scraper:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout repository
        uses: actions/checkout@v3
      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: 3.9
      - name: Install dependencies
        run: |
          python -m pip install --upgrade pip
          pip install -r requirements.txt
      - name: Run scraper script
        run: python script.py
        env:
          TELEGRAM_TOKEN: ${{ secrets.TELEGRAM_TOKEN }}
          TELEGRAM_CHANNEL_ID: ${{ secrets.TELEGRAM_CHANNEL_ID }}
________________________________________
Шаг 5: Добавление секретов (API-ключей)
1.	Перейдите в Settings → Secrets and variables → Actions.
2.	Нажмите New repository secret и создайте первый секрет:
o	Name (Имя): TELEGRAM_TOKEN
o	Secret (Значение): Ваш_Telegram_Токен
o	Нажмите Add secret.
3.	Нажмите New repository secret снова и создайте второй секрет:
o	Name (Имя): TELEGRAM_CHANNEL_ID
o	Secret (Значение): Ваш_ID_Канала
o	Нажмите Add secret.
________________________________________
Шаг 6: Запуск workflow вручную
1.	Перейдите во вкладку Actions в репозитории.
2.	Выберите workflow Manual Scraper Run.
3.	Нажмите Run workflow и дождитесь выполнения.
4.	Перейдите в запущенный workflow и откройте вкладку Logs, чтобы проверить выполнение каждого шага.
________________________________________
Теперь ваш репозиторий полностью настроен для автоматического запуска скрипта через GitHub Actions! 🚀

