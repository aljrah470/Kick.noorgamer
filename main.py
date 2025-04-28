import asyncio
from playwright.async_api import async_playwright
from datetime import datetime, timedelta

USERNAME = "aljrah49"
PASSWORD = "123456789Mmm."
STREAM_URL = "https://kick.com/noorgamer"
WATCH_DURATION_HOURS = 8  # عدد الساعات اللي يبقى فيها يطالع البث

async def login_and_watch():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)  # Headless True عشان يشتغل في Render
        context = await browser.new_context()
        page = await context.new_page()

        # افتح موقع تسجيل الدخول
        await page.goto("https://kick.com/login", timeout=60000)
        await page.fill('input[name="email"]', USERNAME)
        await page.fill('input[name="password"]', PASSWORD)
        await page.click('button:has-text("Login")')
        await page.wait_for_timeout(5000)  # انتظر بعد تسجيل الدخول 5 ثواني

        # افتح رابط البث
        await page.goto(STREAM_URL, timeout=60000)
        print(f"[{datetime.now()}] Watching stream...")

        # خله يطالع البث 8 ساعات
        watch_duration_seconds = WATCH_DURATION_HOURS * 60 * 60
        await page.wait_for_timeout(watch_duration_seconds * 1000)

        print(f"[{datetime.now()}] Finished watching.")
        await browser.close()

def run():
    asyncio.run(login_and_watch())

if __name__ == "__main__":
    run()
