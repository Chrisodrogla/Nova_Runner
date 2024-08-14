import pandas as pd
import time
from selenium import webdriver
from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build
import os
import json
from selenium.common.exceptions import NoSuchElementException
from datetime import datetime


# Google Sheets setup
SHEET_ID = '1S6gAIsjuYyGtOmWFGpF9okAPMWq6SnZ1zbIylBZqCt4'
SHEET_NAME1 = 'Airbnb_Metrics'  # Sheet to clear data below header and write new data

# Load credentials from environment variables
username = os.environ.get('AIRBNB_USER_SECRET')
passw = os.environ.get('AIRBNB_PASSW_SECRET')

if not username or not passw:
    raise ValueError("Airbnb username or password not found in environment variables")

# Get Google Sheets credentials from environment variable
GOOGLE_SHEETS_CREDENTIALS = os.getenv("GOOGLE_SHEETS_CREDENTIALS")
if not GOOGLE_SHEETS_CREDENTIALS:
    raise ValueError("Google Sheets credentials not found in environment variables")

credentials = Credentials.from_service_account_info(json.loads(GOOGLE_SHEETS_CREDENTIALS))

# Create Google Sheets API service
service = build("sheets", "v4", credentials=credentials)

# Set up Chrome WebDriver
options = webdriver.ChromeOptions()
options.add_argument("--headless")
options.add_argument("--disable-dev-shm-usage")
options.add_argument("--no-sandbox")
options.add_argument("--window-size=1920x1080")

driver = webdriver.Chrome(options=options)

# Navigate to Airbnb login page
website = "https://www.airbnb.com/performance/conversion/conversion_rate"
driver.get(website)

# Perform the login
try:
    log = driver.find_element("xpath", """//button[@aria-label="Continue with email"]""")
    log.click()
    time.sleep(2)

    driver.find_element("xpath", """//input[@inputmode="email"]""").send_keys(username)
    time.sleep(2)

    log1 = driver.find_element("xpath", """//button[@data-testid="signup-login-submit-btn"]""")
    log1.click()
    time.sleep(2)

    driver.find_element("xpath", """//input[@name="user[password]"]""").send_keys(passw)
    time.sleep(2)

    log1 = driver.find_element("xpath", """//button[@data-testid="signup-login-submit-btn"]""")
    log1.click()

except NoSuchElementException as e:
    print(f"Login failed: {str(e)}")
    driver.quit()
    raise

time.sleep(10)

# Re-navigate to the target page after login
driver.get(website)
time.sleep(10)

# Retrieve listing IDs
try:
    all_listing = driver.find_element("xpath", """//div[@data-testid="listingPicker"]/button""")
    all_listing.click()
    time.sleep(2)

    lists = driver.find_elements("xpath", """//div[@class="_1a8jl99"]/div/div[1]""")
    Listings = [list_item.get_attribute('id') for list_item in lists]

    print(Listings)

except NoSuchElementException as e:
    print(f"Failed to retrieve listings: {str(e)}")

finally:
    driver.quit()

# Additional logic for processing and updating Google Sheets can go here
