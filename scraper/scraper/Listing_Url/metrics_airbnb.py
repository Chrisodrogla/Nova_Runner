import os
import time
from selenium import webdriver
from selenium.webdriver.firefox.options import Options as FirefoxOptions

# Set environment variables
username = os.environ['AIRBNB_USER_SECRET']
passw = os.environ['AIRBNB_PASSW_SECRET']

website = "https://www.airbnb.com/performance/conversion/conversion_rate"

# Configure Firefox options
options = FirefoxOptions()
options.binary_location = "/usr/bin/firefox"  # Set the correct path to the Firefox binary
options.headless = True  # Enable headless mode for running in environments without a display

# Initialize the WebDriver with the correct options
driver = webdriver.Firefox(options=options)

try:
    # Open the Airbnb website
    driver.get(website)

    # Using the Login to Enter the Airbnb website
    log = driver.find_element("xpath", """//button[@aria-label="Continue with email"]""")
    log.click()
    driver.find_element("xpath", """//input[@inputmode="email"]""").send_keys(username)
    time.sleep(2)
    log1 = driver.find_element("xpath", """//button[@data-testid="signup-login-submit-btn"]""")
    log1.click()
    time.sleep(2)
    driver.find_element("xpath", """//input[@name="user[password]"]""").send_keys(passw)
    time.sleep(2)
    log1 = driver.find_element("xpath", """//button[@data-testid="signup-login-submit-btn"]""")
    log1.click()

    # Method of getting the listing numbers available on the website
    time.sleep(10)
    all_listing = driver.find_element("xpath", """//div[@data-testid="listingPicker"]/button""")
    all_listing.click()
    time.sleep(2)
    lists = driver.find_elements("xpath", """//div[@class="_1a8jl99"]/div/div[1]""")
    Listings = []
    for list_item in lists:
        div_id = list_item.get_attribute('id')
        Listings.append(div_id)

    print(Listings)

finally:
    # Ensure that the driver is properly closed in case of any exceptions
    driver.quit()
