# AlphaScraper

Настройка GitHub Actions для автоматизации выполнения задач

# Цель

Этот документ поможет вам настроить GitHub Actions для автоматизации выполнения задач, таких как тестирование, развертывание или выполнение скриптов. Мы создадим новый репозиторий, добавим рабочий процесс (workflow) и настроим его для ручного запуска.

## План

Создать новый репозиторий на GitHub.

Заполнить информацию о репозитории и выбрать параметры видимости.

Добавить основной скрипт (script.py) в репозиторий.

Создать файл зависимостей requirements.txt.

Создать и настроить GitHub Actions workflow.

Добавить секреты (API-ключи) и запустить workflow вручную.

Проверить успешное выполнение workflow и отладить возможные ошибки.



### Шаг 1: Создание нового репозитория на GitHub

Откройте  и войдите в свой аккаунт.

В верхнем правом углу нажмите на значок “+”.

В выпадающем меню выберите “New repository”.



### Шаг 2: Заполнение информации о репозитории

Owner (Владелец) – Убедитесь, что выбран ваш аккаунт.

Repository name (Имя репозитория) – Введите уникальное имя для вашего проекта.

Description (Описание, необязательно) – Укажите краткое описание проекта, например:

"Этот репозиторий содержит код для автоматизированного сбора данных и отправки уведомлений в Telegram."

Выберите видимость репозитория:

Public – репозиторий будет доступен всем в интернете.

Private – только вы и приглашённые пользователи смогут видеть репозиторий.

Инициализация репозитория (опционально):

Add a README file – добавит файл README.md, в котором можно написать описание проекта.

Add .gitignore – выберите шаблон, если хотите игнорировать определённые файлы (например, для Python можно выбрать Python).



### Шаг 3: Добавление основного скрипта (script.py) и файла зависимостей (requirements.txt) с отладкой

Перейдите в ваш репозиторий на GitHub.

Нажмите на вкладку Code.

Нажмите на значок + справа от вкладки Code, затем выберите Create new file.

В поле имени файла введите script.py.

Перед добавлением основного скрипта важно убедиться, что секреты загружаются корректно. Для этого включим отладочные выводы, которые помогут проверить, правильно ли передаются значения API-токена и ID канала.

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

Нажмите Commit new file, чтобы сохранить файл в репозитории.

Теперь создайте файл requirements.txt, который содержит список зависимостей для скрипта:

В поле имени файла введите requirements.txt.

Вставьте список необходимых библиотек, например:

txt

Копировать

requests

Нажмите Commit new file, чтобы сохранить файл.

Теперь у вас есть оба файла: script.py и requirements.txt, которые необходимы для успешной работы вашего проекта.



### Шаг 4: Настройка GitHub Actions

Создайте папку для workflows:

Перейдите в ваш репозиторий на сайте GitHub.

Нажмите на вкладку Code.

Нажмите на значок + справа от вкладки Code, затем выберите Create new file.

В поле имени файла введите .github/workflows/manual_scraper.yml.

GitHub автоматически создаст необходимые папки, если их ещё нет.

Создайте файл workflow:

В этой папке создайте файл manual_scraper.yml.

Откройте файл и добавьте следующий код:

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



### Шаг 5: Добавление секретов (API-ключей)

Перейдите в Settings → Secrets and variables → Actions.

Нажмите New repository secret и создайте первый секрет:

Name (Имя): TELEGRAM_TOKEN

Secret (Значение): Ваш_Telegram_Токен

Нажмите Add secret.

Нажмите New repository secret снова и создайте второй секрет:

Name (Имя): TELEGRAM_CHANNEL_ID

Secret (Значение): Ваш_ID_Канала

Нажмите Add secret.



### Шаг 6: Запуск workflow вручную

Перейдите во вкладку Actions в репозитории.

Выберите workflow Manual Scraper Run.

Нажмите Run workflow и дождитесь выполнения.

Перейдите в запущенный workflow и откройте вкладку Logs, чтобы проверить выполнение каждого шага.



## Заключение

Теперь ваш репозиторий полностью настроен для автоматического запуска скрипта через GitHub Actions! 🚀


