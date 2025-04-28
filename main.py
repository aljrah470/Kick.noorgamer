from flask import Flask
import threading
import os
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

app = Flask(__name__)

def start_bot():
    print("جاري تشغيل البوت ومحاولة الدخول إلى البث...")
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    
    driver = None
    try:
        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=options)
        
        driver.get("https://kick.com/")  # حط رابط البث هنا لو تبي
        time.sleep(5)  # انتظر 5 ثواني عشان يتأكد فتح الصفحة
        print("تم تشغيل البوت بنجاح!")
        
    except Exception as e:
        print("حدث خطأ أثناء تشغيل البوت:", e)
    finally:
        if driver:
            driver.quit()

@app.route('/')
def home():
    return "البوت شغال!"

if __name__ == "__main__":
    threading.Thread(target=start_bot).start()
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
