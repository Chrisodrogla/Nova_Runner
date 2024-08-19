import os
import asyncio
from pyppeteer import launch

async def main():
    username = os.environ['AIRBNB_USER_SECRET']
    passw = os.environ['AIRBNB_PASSW_SECRET']
    website = "https://www.airbnb.com/performance/conversion/conversion_rate"

    browser = await launch(headless=True, args=['--no-sandbox', '--disable-dev-shm-usage'])
    page = await browser.newPage()
    await page.goto(website)

    await page.click('button[aria-label="Continue with email"]')
    await page.type('input[inputmode="email"]', username)
    current_html = await page.content()
    print(current_html)

    await asyncio.sleep(2)
    await page.click('button[data-testid="signup-login-submit-btn"]')
    await asyncio.sleep(2)

    await browser.close()

asyncio.run(main())
