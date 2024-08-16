import os
import time
from playwright.sync_api import sync_playwright

start_time = time.time()

username = os.environ['AIRBNB_USER_SECRET']
passw = os.environ['AIRBNB_PASSW_SECRET']

website = "https://www.airbnb.com/performance/conversion/conversion_rate"

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)  # Use headless mode
    context = browser.new_context()
    page = context.new_page()
    page.goto(website)

    # Login process
    page.click('button[aria-label="Continue with email"]')
    page.fill('input[inputmode="email"]', username)
    page.click('button[data-testid="signup-login-submit-btn"]')
    time.sleep(2)
    page.fill('input[name="user[password]"]', passw)
    page.click('button[data-testid="signup-login-submit-btn"]')

    # Add any additional scraping logic here

    browser.close()
