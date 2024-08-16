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

start_time = time.time()

username = os.environ['AIRBNB_USER_SECRET']
passw = os.environ['AIRBNB_PASSW_SECRET']

website = "https://www.airbnb.com/performance/conversion/conversion_rate"

# Set up Firefox WebDriver
options = webdriver.FirefoxOptions()
# options.add_argument("--headless")  # Uncomment this if you want to run in headless mode
options.add_argument("--disable-dev-shm-usage")
options.add_argument("--no-sandbox")
# options.add_argument("--disable-gpu")
options.add_argument("--window-size=1920x1080")

driver = webdriver.Firefox(options=options)
driver.get(website)

# Using the Login to Enter the Airbnb websites first so the data becomes available
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
