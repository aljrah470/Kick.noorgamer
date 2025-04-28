import threading
from flask import Flask
import time
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

app = Flask(__name__)

def start_bot():
    driver = None
    try:
        print("جاري تشغيل البوت ومحاولة الدخول إلى البث...")
        
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        driver = webdriver.Chrome(options=chrome_options)

        # هنا تحط الكود الخاص بتصفح الموقع والدخول للبث

    except Exception as e:
        print(f"حدث خطأ: {e}")
    finally:
        if driver:
            driver.quit()

@app.route('/')
def index():
    return "البوت شغال!"

def wait_until_target_time():
    while True:
        now = datetime.now()
        current_time = now.strftime("%H:%M:%S")
        print(f"الوقت الآن {current_time} بتوقيت السعودية. في انتظار الساعة 10 مساءً...")

        if now.hour >= 22:  # الساعة 10 مساء
            break

        time.sleep(30)  # ينتظر 30 ثانية قبل التحقق مرة ثانية

if __name__ == '__main__':
    wait_until_target_time()
    threading.Thread(target=start_bot).start()
    app.run(host="0.0.0.0", port=10000)
