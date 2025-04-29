from apify_client import ApifyClient
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
import time, pickle, os

USERNAME = "aljrah49"
PASSWORD = "123456789Mmm."
STREAM_URL = "https://kick.com/noorgamer"

def login(driver):
    driver.get("https://kick.com/login")
    time.sleep(5)
    username_input = driver.find_element(By.NAME, "username")
    password_input = driver.find_element(By.NAME, "password")
    login_button = driver.find_element(By.XPATH, "//button[contains(text(), 'Log In')]")
    username_input.send_keys(USERNAME)
    password_input.send_keys(PASSWORD)
    login_button.click()
    time.sleep(8)
    with open("cookies.pkl", "wb") as f:
        pickle.dump(driver.get_cookies(), f)

def load_cookies(driver):
    if os.path.exists("cookies.pkl"):
        with open("cookies.pkl", "rb") as f:
            cookies = pickle.load(f)
            for cookie in cookies:
                driver.add_cookie(cookie)

def is_stream_live(driver):
    try:
        offline_text = driver.find_elements(By.XPATH, "//div[contains(text(), 'offline') or contains(text(), 'Offline')]")
        return len(offline_text) == 0
    except:
        return False

def main():
    options = Options()
    options.add_argument("--headless=new")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-blink-features=AutomationControlled")

    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)

    try:
        driver.get("https://kick.com/")
        time.sleep(5)
        if os.path.exists("cookies.pkl"):
            load_cookies(driver)
            driver.refresh()
            time.sleep(5)
        else:
            login(driver)

        driver.get(STREAM_URL)
        time.sleep(5)

        if is_stream_live(driver):
            print("✅ البث مباشر، تم احتساب نقطة.")
        else:
            print("❌ البث غير مباشر.")
    except Exception as e:
        print("حدث خطأ:", e)
    finally:
        driver.quit()

if __name__ == "__main__":
    main()
