import os
import asyncio
from pyppeteer import launch
import logging

logging.basicConfig(level=logging.INFO)

async def main():
    username = os.environ.get('AIRBNB_USER_SECRET')
    passw = os.environ.get('AIRBNB_PASSW_SECRET')

    if not username or not passw:
        logging.error("Environment variables for Airbnb credentials are not set.")
        return

    website = "https://www.airbnb.com/performance/conversion/conversion_rate"

    try:
        # Set up Pyppeteer
        browser = await launch({
            'headless': False,  # Set to True to run headless
            'args': ['--no-sandbox', '--disable-dev-shm-usage', '--window-size=1920x1080']
        })
        page = await browser.newPage()
        await page.goto(website)

        # Using the Login to Enter the Airbnb website
        await page.click('button[aria-label="Continue with email"]')
        await page.type('input[inputmode="email"]', username)
        await page.click('button[data-testid="signup-login-submit-btn"]')
        await page.waitForTimeout(2000)  # Wait for 2 seconds

        # Capture the page source
        content = await page.content()
        print(content)

    except Exception as e:
        logging.error(f"An error occurred: {e}")

    finally:
        if 'browser' in locals():
            await browser.close()

# Run the async function
if __name__ == "__main__":
    asyncio.get_event_loop().run_until_complete(main())
