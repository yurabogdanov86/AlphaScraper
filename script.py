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
# 🔹 Конфигурация логирования
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
# 🔹 Конфигурация Telegram бота
# (читаем из переменных окружения)
# -----------------------------------
TOKEN = os.getenv("TELEGRAM_TOKEN")
CHANNEL_ID = os.getenv("TELEGRAM_CHANNEL_ID")

FILE_PATH = "previous_value.txt"  # Файл для хранения предыдущего значения

def send_telegram_message(text):
    """Функция отправки сообщения в Telegram"""
    if not TOKEN or not CHANNEL_ID:
        logging.error("❌ Ошибка: TELEGRAM_TOKEN или TELEGRAM_CHANNEL_ID не найдены в переменных окружения.")
        return

    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    data = {
        "chat_id": CHANNEL_ID,
        "text": text,
        "parse_mode": "Markdown"
    }

    response = requests.post(url, data=data)
    if response.status_code == 200:
        logging.info("✅ Сообщение успешно отправлено в Telegram!")
    else:
        logging.error(f"❌ Ошибка отправки! Код ответа: {response.status_code}, Текст: {response.text}")

def read_previous_value():
    """Читает предыдущее значение ставки риска из файла"""
    if os.path.exists(FILE_PATH):
        with open(FILE_PATH, "r", encoding="utf-8") as file:
            return file.read().strip()
    return None  # Если файла нет, значит данных ещё нет

def write_new_value(value):
    """Записывает новое значение ставки риска в файл"""
    with open(FILE_PATH, "w", encoding="utf-8") as file:
        file.write(value)

def main():
    """Основная функция выполнения парсинга"""
    options = webdriver.ChromeOptions()
    options.add_argument("--start-maximized")
    options.add_argument("--disable-gpu")
    options.headless = True  # Без GUI, полезно для GitHub Actions
    
    driver = webdriver.Chrome(options=options)

    try:
        url = "https://alfabank.ru/make-money/investments/help/trebuemoe-obespechenie/"
        logging.info("Открываем страницу: %s", url)
        driver.get(url)
        
        WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.TAG_NAME, "body")))
        logging.info("Страница загружена. BODY найден.")

        # Прокручиваем страницу, чтобы кнопка 'Фонды' стала видимой
        for _ in range(3):
            driver.execute_script("window.scrollBy(0, 200);")
            time.sleep(1)
        logging.info("Прокрутили страницу вниз для видимости кнопки 'Фонды'.")

        # Ищем и кликаем по кнопке 'Фонды'
        try:
            fund_button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//span[contains(text(), 'Фонды')]"))
            )
            ActionChains(driver).move_to_element(fund_button).perform()
            time.sleep(1)
            fund_button.click()
            logging.info("✅ Кнопка 'Фонды' успешно нажата!")
        except Exception as e:
            logging.error(f"❌ Не удалось найти или нажать кнопку 'Фонды': {e}")
            return
        
        logging.info("⏳ Ждём 5 секунд для полной загрузки данных...")
        time.sleep(5)

        xpath_expr = "//p[@data-test-id='text' and contains(@class, '_8QWkTE')]"
        data_elements = driver.find_elements(By.XPATH, xpath_expr)

        extracted_data = [el.text.strip() for el in data_elements if el.text.strip()]
        
        logging.info("Найдено %d элементов с классом '_8QWkTE': %s", len(extracted_data), extracted_data)

        if len(extracted_data) >= 6:
            current_risk_rate = extracted_data[3]  # Ставка риска длинные позиции (текущая)
            previous_risk_rate = read_previous_value()

            if previous_risk_rate is None or current_risk_rate != previous_risk_rate:
                message = f"""🔹 *Обновление ставки риска!* 🚨
1. {extracted_data[0]}
2. *ISIN:* {extracted_data[1]}
3. *Валюта риска:* {extracted_data[2]}
4. *Ставка риска (длинные позиции, текущая):* {current_risk_rate} (было: {previous_risk_rate if previous_risk_rate else "нет данных"})
5. *Ставка риска (длинные позиции, начальная):* {extracted_data[4]}
6. *Ставка риска (короткие позиции, начальная):* {extracted_data[5]}
"""
                send_telegram_message(message)
                write_new_value(current_risk_rate)  # Сохраняем новое значение
            else:
                logging.info("📊 Ставка риска не изменилась, сообщение не отправляем.")
        else:
            logging.warning("❌ Не хватает значений! Всего элементов: %d", len(extracted_data))
            for i, val in enumerate(extracted_data, start=1):
                logging.warning("%d. %s", i, val)

    finally:
        driver.quit()
        logging.info("Закрываем браузер и завершаем работу.")

if __name__ == "__main__":
    main()
