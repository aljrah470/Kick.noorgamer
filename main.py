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
from status_manager import save_status, load_status

app = Flask(__name__)
bot_thread = None

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
    for _ in range(1):
        x_offset = random.randint(-100, 100)
        y_offset = random.randint(-100, 100)
        try:
            actions.move_by_offset(x_offset, y_offset).perform()
            actions.reset_actions()
            time.sleep(random.uniform(1, 2))
        except Exception:
            pass

def is_stream_live(driver):
    try:
        offline_text = driver.find_elements(By.XPATH, "//div[contains(text(), 'offline') or contains(text(), 'Offline')]")
        return len(offline_text) == 0
    except Exception:
        return False

def start_bot():
    status = load_status()
    bot_running = True
    watching = status["watching"]
    points = status["points"]
    start_timestamp = status["start_timestamp"] or time.time()

    options = Options()
    options.add_argument("--headless=new")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-blink-features=AutomationControlled")

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

        while load_status()["bot_running"] and (time.time() - start_timestamp < 8 * 60 * 60):
            driver.get(STREAM_URL)
            time.sleep(5)

            watching = is_stream_live(driver)
            if watching:
                print("✅ يشاهد البث الآن.")
                points += 1
            else:
                print("⌛ البث غير متاح حالياً...")

            save_status(True, watching, points, start_timestamp)
            random_human_behavior(driver)
            time.sleep(60)

    except Exception as e:
        print("❌ حصل خطأ:", e)
    finally:
        if driver:
            driver.quit()
        save_status(False, False, points, 0)
        print("🛑 تم إيقاف البوت.")

@app.route('/')
def index():
    status = load_status()
    elapsed_minutes = int((time.time() - status["start_timestamp"]) / 60) if status["bot_running"] else 0
    return render_template('index.html',
                           bot_running=status["bot_running"],
                           elapsed_minutes=elapsed_minutes,
                           watching=status["watching"],
                           points=status["points"])

@app.route('/start')
def start():
    status = load_status()
    if not status["bot_running"]:
        save_status(True, False, status["points"], time.time())
        global bot_thread
        bot_thread = threading.Thread(target=start_bot)
        bot_thread.start()
    return redirect(url_for('index'))

@app.route('/stop')
def stop():
    status = load_status()
    save_status(False, False, status["points"], 0)
    return redirect(url_for('index'))

@app.route('/reset')
def reset():
    status = load_status()
    save_status(status["bot_running"], status["watching"], 0, status["start_timestamp"])
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
