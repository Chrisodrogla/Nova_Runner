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

    # Wait for the page to fully load after login
    page.wait_for_load_state('networkidle')

    # Write the HTML content to a file
    page_html = page.content()
    with open('/tmp/page_content.html', 'w') as file:
        file.write(page_html)

    # # Wait for the listings picker to be available
    # time.sleep(10)  # Adjust as necessary for your page
    #
    # # Click the button to open the listing picker
    # page.click('div[data-testid="listingPicker"] button')
    #
    # # Wait for the listings to be available
    # time.sleep(2)  # Adjust as necessary for your page
    #
    # # Extract listing IDs
    # listing_elements = page.query_selector_all('div._1a8jl99 > div > div:first-of-type')
    # listings = []
    # for element in listing_elements:
    #     div_id = element.get_attribute('id')
    #     if div_id:
    #         listings.append(div_id)
    #
    # # Print the listing IDs
    # print("Listings IDs:")
    # for listing in listings:
    #     print(listing)

    # Close the browser
    browser.close()
