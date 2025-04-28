from flask import Flask
import os
import threading
import time
import datetime
import pytz  # <-- مكتبة التوقيتات
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

# بيانات الحساب
username = "aljrah49"
password = "123456789Mmm"
stream_url = "https://kick.com/noorgamer"

# توقيت السعودية
saudi_tz = pytz.timezone('Asia/Riyadh')

def wait_until_10pm_saudi():
    while True:
        now = datetime.datetime.now(saudi_tz)
        if now.hour == 22:
            print("حان وقت الدخول إلى البث (الساعة 10 مساءً بتوقيت السعودية)!")
            break
        else:
            seconds_until_next_minute = 60 - now.second
            print(f"الوقت الآن {now.strftime('%H:%M:%S')} بتوقيت السعودية. في انتظار الساعة 10 مساءً...")
            time.sleep(seconds_until_next_minute)

def start_bot():
    while True:
        driver = None
        try:
            wait_until_10pm_saudi()

            print("جاري تشغيل البوت ومحاولة الدخول إلى البث...")
            options = webdriver.ChromeOptions()
            options.add_argument("--headless=new")
            options.add_argument("--no-sandbox")
            options.add_argument("--disable-dev-shm-usage")
            options.add_argument("--disable-gpu")
            options.add_argument("--window-size=1920,1080")

            service = Service(ChromeDriverManager().install())
            driver = webdriver.Chrome(service=service, options=options)

            driver.get("https://kick.com/login")
            time.sleep(5)

            driver.find_element(By.NAME, "username").send_keys(username)
            driver.find_element(By.NAME, "password").send_keys(password)
            driver.find_element(By.NAME, "password").send_keys(Keys.RETURN)

            time.sleep(7)

            driver.get(stream_url)
            print("تم تسجيل الدخول والدخول للبث بنجاح!")

            # البقاء على البث لمدة 8 ساعات
            time.sleep(8 * 60 * 60)

        except Exception as e:
            print(f"حدث خطأ: {e}")
        finally:
            if driver:
                driver.quit()

        print("إعادة المحاولة في اليوم التالي...")
        # ننتظر حتى اليوم الثاني
        time.sleep(60)

app = Flask(__name__)

@app.route('/')
def home():
    return "البوت شغال ويتابع البث!!"

if __name__ == '__main__':
    threading.Thread(target=start_bot).start()

    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)
