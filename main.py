import asyncio
from playwright.async_api import async_playwright
import datetime

USER_EMAIL = "aljrah49"
USER_PASSWORD = "123456789Mmm."
WATCH_URL = "https://kick.com/noorgamer"

# مدة المشاهدة بالثواني (8 ساعات = 8 * 60 * 60)
WATCH_DURATION = 8 * 60 * 60

async def login_and_watch():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True, args=["--no-sandbox"])
        page = await browser.new_page()

        # افتح موقع Kick
        await page.goto("https://kick.com")

        # اضغط تسجيل الدخول
        await page.click('text=Log In')

        # اكتب الإيميل والباسوورد
        await page.fill('input[name="email"]', USER_EMAIL)
        await page.fill('input[name="password"]', USER_PASSWORD)

        # اضغط تسجيل الدخول
        await page.click('button:has-text("Log In")')

        # انتظر شوي للتأكد من تسجيل الدخول
        await page.wait_for_timeout(5000)

        # رح للبث المطلوب
        await page.goto(WATCH_URL)

        # خلي الصفحة مفتوحة لمدة المشاهدة المطلوبة
        print(f"Started watching at {datetime.datetime.now()}")
        await page.wait_for_timeout(WATCH_DURATION * 1000)
        print(f"Finished watching at {datetime.datetime.now()}")

        await browser.close()

def run():
    asyncio.run(login_and_watch())

if __name__ == "__main__":
    run()
