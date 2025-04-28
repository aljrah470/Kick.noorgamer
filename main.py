from flask import Flask
import os
import threading
import time
import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

# بيانات الحساب
username = "aljrah49"
password = "123456789Mmm"
stream_url = "https://kick.com/noorgamer"

def start_bot():
    while True:
        try:
            print("جاري تشغيل البوت ومحاولة الدخول إلى البث...")
            options = webdriver.ChromeOptions()
            options.add_argument("--headless")
            options.add_argument("--no-sandbox")
            options.add_argument("--disable-dev-shm-usage")

            service = Service(ChromeDriverManager().install())
            driver = webdriver.Chrome(service=service, options=options)

            driver.get("https://kick.com/login")
            time.sleep(5)

            driver.find_element(By.NAME, "username").send_keys(username)
            driver.find_element(By.NAME, "password").send_keys(password)
            driver.find_element(By.NAME, "password").send_keys(Keys.RETURN)

            time.sleep(7)

            driver.get(stream_url)
            print("تم تسجيل الدخول بنجاح والدخول للبث!")

            # البقاء لمدة 8 ساعات
            time.sleep(8 * 60 * 60)

        except Exception as e:
            print(f"حدث خطأ: {e}")
        finally:
            driver.quit()

        # إعادة المحاولة بعد دقيقة لو صار خطأ
        time.sleep(60)

app = Flask(__name__)

@app.route('/')
def home():
    return "البوت شغال ويتابع البث!!"

if __name__ == '__main__':
    threading.Thread(target=start_bot).start()

    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)
