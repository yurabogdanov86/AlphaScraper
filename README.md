
# Инструкция по настройке автоматизации с помощью GitHub Actions

Эта инструкция поможет вам настроить автоматизацию с помощью **GitHub Actions**, чтобы выполнять задачу парсинга и отправки уведомлений в Telegram. В процессе будут использоваться **Selenium** для автоматизированного сбора данных, **Telegram-бот** для уведомлений, и **GitHub Actions** для автоматизации процесса.

---

### **Шаг 1: Создание репозитория на GitHub**
1. Откройте **GitHub** и войдите в свой аккаунт.
2. Нажмите на значок **“+”** в верхнем правом углу и выберите **New repository**.
3. Укажите **имя** репозитория (например, `AlphaScraper`), выберите видимость (Public или Private) и нажмите **Create repository**.

---

### **Шаг 2: Настройка проекта**
1. В вашем репозитории создайте следующие файлы:
   - `script.py` — основной Python-скрипт для парсинга и отправки данных в Telegram.
   - `requirements.txt` — файл, содержащий список зависимостей, необходимых для работы скрипта.

2. Пример содержимого `script.py`:

```python
import logging
import time
import requests
import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# -----------------------------------
# Конфигурация логирования
# -----------------------------------
logging.basicConfig(
    filename='scraper.log',
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s [%(levelname)s] %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
console_handler.setFormatter(formatter)
logging.getLogger().addHandler(console_handler)

# -----------------------------------
# Конфигурация Telegram бота
# -----------------------------------
TOKEN = os.getenv("TELEGRAM_TOKEN")
CHANNEL_ID = os.getenv("TELEGRAM_CHANNEL_ID")

FILE_PATH = "previous_value.txt"  # Файл для хранения предыдущего значения

def send_telegram_message(text):
    if not TOKEN or not CHANNEL_ID:
        logging.error("Ошибка: TELEGRAM_TOKEN или TELEGRAM_CHANNEL_ID не найдены в переменных окружения.")
        return

    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    data = {
        "chat_id": CHANNEL_ID,
        "text": text,
        "parse_mode": "Markdown"
    }

    response = requests.post(url, data=data)
    if response.status_code == 200:
        logging.info("Сообщение успешно отправлено в Telegram!")
    else:
        logging.error(f"Ошибка отправки! Код ответа: {response.status_code}, Текст: {response.text}")

def read_previous_value():
    if os.path.exists(FILE_PATH):
        with open(FILE_PATH, "r", encoding="utf-8") as file:
            return file.read().strip()
    return None

def write_new_value(value):
    with open(FILE_PATH, "w", encoding="utf-8") as file:
        file.write(value)

def main():
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")  # Запуск без GUI
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-gpu")
    options.add_argument("--user-data-dir=/tmp/chrome-user-data")
    options.add_argument("--disable-blink-features=AutomationControlled")

    driver = webdriver.Chrome(options=options)

    try:
        url = "https://alfabank.ru/make-money/investments/help/trebuemoe-obespechenie/"
        logging.info("Открываем страницу: %s", url)
        driver.get(url)
        
        WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.TAG_NAME, "body")))
        logging.info("Страница загружена.")

        for _ in range(3):
            driver.execute_script("window.scrollBy(0, 200);")
            time.sleep(1)
        logging.info("Прокрутили страницу вниз.")

        try:
            fund_button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//span[contains(text(), 'Фонды')]"))
            )
            ActionChains(driver).move_to_element(fund_button).perform()
            time.sleep(1)
            fund_button.click()
            logging.info("Кнопка 'Фонды' нажата!")
        except Exception as e:
            logging.error(f"Не удалось нажать кнопку 'Фонды': {e}")
            return
        
        logging.info("Ждем 5 секунд...")
        time.sleep(5)

        xpath_expr = "//p[@data-test-id='text' and contains(@class, '_8QWkTE')]"
        data_elements = driver.find_elements(By.XPATH, xpath_expr)

        extracted_data = [el.text.strip() for el in data_elements if el.text.strip()]
        
        logging.info("Найдено %d элементов.", len(extracted_data))

        if len(extracted_data) >= 6:
            current_risk_rate = extracted_data[3]
            previous_risk_rate = read_previous_value()

            if previous_risk_rate is None or current_risk_rate != previous_risk_rate:
                message = f"Обновление ставки риска! 
1. {extracted_data[0]} 
2. ISIN: {extracted_data[1]} 
3. Валюта: {extracted_data[2]} 
4. Ставка риска: {current_risk_rate} (до: {previous_risk_rate if previous_risk_rate else 'нет данных'})"
                send_telegram_message(message)
                write_new_value(current_risk_rate)
            else:
                logging.info("Ставка не изменилась.")
        else:
            logging.warning("Недостаточно данных.")

    finally:
        driver.quit()
        logging.info("Завершаем работу.")

if __name__ == "__main__":
    main()
```

3. Пример содержимого `requirements.txt`:
```
requests
selenium
chromedriver-autoinstaller
```

---

### **Шаг 3: Настройка GitHub Actions для автоматизации**
1. В репозитории создайте папку `.github/workflows` и создайте файл `manual_scraper.yml`.
2. Пример содержимого `manual_scraper.yml`:

```yaml
name: Automated Scraper Run

on:
  workflow_dispatch:
  schedule:
    - cron: "0 * * * *"  # Запуск каждый час

permissions:
  contents: write  # Разрешает workflow коммитить файлы в репозиторий

jobs:
  run-scraper:
    runs-on: ubuntu-latest  # Запуск на сервере Ubuntu
    steps:
      # 1️⃣ Клонируем репозиторий
      - name: Checkout repository
        uses: actions/checkout@v3
        with:
          persist-credentials: true

      # 2️⃣ Устанавливаем Chrome (если его нет)
      - name: Install Chrome
        run: |
          sudo apt-get update
          sudo apt-get install -y google-chrome-stable

      # 3️⃣ Устанавливаем Python
      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: 3.9

      # 4️⃣ Устанавливаем зависимости
      - name: Install dependencies
        run: |
          python -m pip install --upgrade pip
          pip install -r requirements.txt

      # 5️⃣ Запускаем скрипт
      - name: Run scraper script
        run: python script.py
        env:
          TELEGRAM_TOKEN: ${{ secrets.TELEGRAM_TOKEN }}
          TELEGRAM_CHANNEL_ID: ${{ secrets.TELEGRAM_CHANNEL_ID }}

      # 6️⃣ Коммитим изменения в previous_value.txt (если файл изменился)
      - name: Commit changes
        run: |
          if git diff --quiet; then
            echo "No changes detected. Skipping commit."
          else
            echo "Changes detected. Committing..."
            git config --global user.name 'github-actions[bot]'
            git config --global user.email 'github-actions[bot]@users.noreply.github.com'
            git add previous_value.txt
            git commit -m "Update previous_value.txt"
            git push
          fi
```

---

### **Шаг 4: Настройка переменных окружения (Secrets)**
1. В **GitHub** перейдите в настройки репозитория.
2. В разделе **Settings → Secrets and variables → Actions** добавьте:
   - `TELEGRAM_TOKEN` (значение: ваш токен Telegram-бота)
   - `TELEGRAM_CHANNEL_ID` (значение: ID вашего канала или чата)

---

### **Шаг 5: Запуск и мониторинг**
1. Запустите workflow вручную через вкладку **Actions**.
2. Через **cron** workflow будет запускаться **каждый час**.

---

