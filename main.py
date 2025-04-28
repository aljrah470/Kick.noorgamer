from flask import Flask
import os
import threading
import time
import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager

# بيانات الحساب
username = "aljrah49"
password = "123456789Mmm"
stream_url = "https://kick.com/noorgamer"

def start_bot():
    while True:
        now = datetime.datetime.now()

        # نتحقق هل الساعة 6:00 مساءً
        if now.hour == 18 and now.minute == 0:
            options = webdriver.ChromeOptions()
            options.add_argument("--headless")
            options.add_argument("--no-sandbox")
            options.add_argument("--disable-dev-shm-usage")

            driver = webdriver.Chrome(ChromeDriverManager().install(), options=options)

            try:
                driver.get("https://kick.com/login")
                time.sleep(5)

                driver.find_element(By.NAME, "username").send_keys(username)
                driver.find_element(By.NAME, "password").send_keys(password)
                driver.find_element(By.NAME, "password").send_keys(Keys.RETURN)

                time.sleep(7)

                driver.get(stream_url)
                print("تم الدخول للبث!")

                # البقاء لمدة 8 ساعات
                time.sleep(8 * 60 * 60)

            except Exception as e:
                print(f"حدث خطأ: {e}")
            finally:
                driver.quit()

        # ننتظر دقيقة ونتحقق مرة ثانية
        time.sleep(60)

app = Flask(__name__)

@app.route('/')
def home():
    return "البوت شغال وينتظر الساعة 6 مساءً!"

if __name__ == '__main__':
    threading.Thread(target=start_bot).start()

    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)
