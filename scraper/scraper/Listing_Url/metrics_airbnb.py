import os
import time
import datetime
from selenium import webdriver
import shutil
import json
from selenium.common.exceptions import NoSuchElementException
import datetime
import pytz
import pandas as pd
from datetime import datetime, timedelta
import calendar



username ="data.bnb@NovaVacation.com"
passw = "Data@2024*"


website = "https://www.airbnb.com/performance/conversion/conversion_rate"

# # Set up Chrome WebDriver
# options = webdriver.ChromeOptions()
# options.add_argument("--headless")
# options.add_argument("--disable-dev-shm-usage")
# options.add_argument("--no-sandbox")
# options.add_argument("--disable-gpu")
# options.add_argument("--window-size=1920x1080")
options = webdriver.ChromeOptions()
options.add_argument("--headless")  # Still run headless, but we'll try to mimic a normal browser
options.add_argument("--disable-dev-shm-usage")
options.add_argument("--no-sandbox")
options.add_argument("--disable-gpu")
options.add_argument("--window-size=1920x1080")

# Additional options to avoid detection
options.add_argument("--start-maximized")  # Start maximized to mimic a real browser window
options.add_argument("--disable-blink-features=AutomationControlled")  # Disable automation detection
options.add_argument("--incognito")  # Start in incognito mode

# Add a realistic user-agent string
options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36")

# Disable WebDriver visibility
options.add_experimental_option("excludeSwitches", ["enable-automation"])
options.add_experimental_option('useAutomationExtension', False)

# Set preferences to reduce detection
prefs = {
    "profile.default_content_setting_values.notifications": 2,  # Disable notifications
    "credentials_enable_service": False,  # Disable password manager
    "profile.password_manager_enabled": False
}
options.add_experimental_option("prefs", prefs)


driver = webdriver.Chrome(options=options)
driver.get(website)
time.sleep(5)

# Using the Login to Enter the Airbnb website
log=driver.find_element("xpath", """//button[@aria-label="Continue with email"]""")
log.click()
driver.find_element("xpath", """//input[@inputmode="email"]""" ).send_keys(username)
time.sleep(2)
log1=driver.find_element("xpath", """//button[@data-testid="signup-login-submit-btn"]""")
log1.click()
time.sleep(2)
driver.find_element("xpath", """//input[@name="user[password]"]""" ).send_keys(passw)
time.sleep(2)
log3=driver.find_element("xpath", """//div[@class="_1kkyzxv"]/button""")
log3.click()
log2=driver.find_element("xpath", """//button[@data-testid="signup-login-submit-btn"]""")
log2.click()
time.sleep(2)



html_content = driver.page_source
print(html_content)

# MEthod of getting the listing numbers available on the website
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