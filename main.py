import time
import chromedriver_autoinstaller
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

# بيانات تسجيل الدخول
username = "aljrah49"
password = "123456789Mmm"
stream_url = "https://kick.com/noorgamer"

# تثبيت نسخة متوافقة مع السيرفر من الكروم درايفر
chromedriver_autoinstaller.install()

options = webdriver.ChromeOptions()
options.add_argument("--headless")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")

driver = webdriver.Chrome(options=options)

try:
    driver.get("https://kick.com/login")
    time.sleep(5)

    driver.find_element(By.NAME, "username").send_keys(username)
    driver.find_element(By.NAME, "password").send_keys(password)
    driver.find_element(By.NAME, "password").send_keys(Keys.RETURN)

    time.sleep(7)

    driver.get(stream_url)
    print("تم الدخول للبث!")

    time.sleep(8 * 60 * 60)

finally:
    driver.quit()
