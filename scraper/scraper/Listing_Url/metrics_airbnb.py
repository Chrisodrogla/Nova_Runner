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

    # Using the Login to Enter the Airbnb website
    await page.click('button[aria-label="Continue with email"]')
    await page.type('input[inputmode="email"]', username)
    await asyncio.sleep(2)
    await page.click('button[data-testid="signup-login-submit-btn"]')
    await asyncio.sleep(2)

    # Entering the password
    await page.type('input[name="user[password]"]', passw)
    await asyncio.sleep(2)
    await page.click('button[data-testid="signup-login-submit-btn"]')
    await asyncio.sleep(2)

    # Optionally capture the page content after login
    current_html = await page.content()
    print(current_html)

    await browser.close()

asyncio.run(main())
