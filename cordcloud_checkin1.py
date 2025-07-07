import asyncio
from playwright.async_api import async_playwright
import urllib.parse
import os

EMAIL = os.getenv("CC_EMAIL")
PASSWD = os.getenv("CC_PASSWD")
LOGIN_URL = "https://www.cordcloud.biz/auth/login"

async def login_and_checkin():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context()
        page = await context.new_page()

        await page.goto("https://www.cordcloud.biz/auth/login")
        await page.fill('input[name="email"]', EMAIL)
        await page.fill('input[name="passwd"]', PASSWD)
        await page.click('button[type="submit"]')

        await page.wait_for_timeout(3000)
        content = await page.content()

        if "登出" in content or "logout" in content.lower():
            print("✅ 登录成功！")

            # 尝试签到
            await page.goto("https://www.cordcloud.biz/user/checkin")
            await page.wait_for_timeout(1000)
            print("✅ 签到已尝试，检查流量页面确认效果。")
        else:
            print("❌ 登录失败，可能是验证码、Cloudflare 防护等问题。")

        await browser.close()

asyncio.run(login_and_checkin())

