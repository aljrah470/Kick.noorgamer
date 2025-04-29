from flask import Flask, render_template, redirect, url_for
import threading
import os
import time
import pickle
import random
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from webdriver_manager.chrome import ChromeDriverManager

app = Flask(__name__)
bot_thread = None
bot_running = False
start_timestamp = 0

USERNAME = "aljrah49"
PASSWORD = "123456789Mmm."
STREAM_URL = "https://kick.com/noorgamer"

def save_cookies(driver, path="cookies.pkl"):
    with open(path, "wb") as file:
        pickle.dump(driver.get_cookies(), file)

def load_cookies(driver, path="cookies.pkl"):
    with open(path, "rb") as file:
        cookies = pickle.load(file)
        for cookie in cookies:
            driver.add_cookie(cookie)

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
    save_cookies(driver)

def random_human_behavior(driver):
    actions = ActionChains(driver)
    for _ in range(1, 2):
        x_offset = random.randint(-100, 100)
        y_offset = random.randint(-100, 100)
        try:
            actions.move_by_offset(x_offset, y_offset).perform()
            actions.reset_actions()
            time.sleep(random.uniform(1, 2))
        except Exception:
            pass

def start_bot():
    global bot_running
    options = Options()
    options.add_argument("--headless=new")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-blink-features=AutomationControlled")

    # السطر المهم عشان تحدد مكان الكروم في Render
    options.binary_location = "/usr/bin/google-chrome"

    driver = None
    try:
        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=options)

        driver.get("https://kick.com/")
        time.sleep(5)

        if os.path.exists("cookies.pkl"):
            load_cookies(driver)
            driver.refresh()
            time.sleep(5)
        else:
            login(driver)

        driver.get(STREAM_URL)
        print("✅ دخل البث بنجاح!")

        start_time = time.time()
        while bot_running and (time.time() - start_time < 8 * 60 * 60):
            random_human_behavior(driver)
            time.sleep(random.randint(30, 60))

    except Exception as e:
        print("❌ حصل خطأ:", e)
    finally:
        if driver:
            driver.quit()
        bot_running = False
        print("🛑 تم إيقاف البوت.")

@app.route('/')
def index():
    global bot_running, start_timestamp
    return render_template('index.html', bot_running=bot_running, start_time=int(start_timestamp) if bot_running else None)

@app.route('/start')
def start():
    global bot_running, bot_thread, start_timestamp
    if not bot_running:
        bot_running = True
        start_timestamp = time.time()
        bot_thread = threading.Thread(target=start_bot)
        bot_thread.start()
    return redirect(url_for('index'))

@app.route('/stop')
def stop():
    global bot_running
    bot_running = False
    return redirect(url_for('index'))
