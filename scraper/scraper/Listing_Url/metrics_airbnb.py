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
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

start_time = time.time()

username = os.environ['AIRBNB_USER_SECRET']
passw = os.environ['AIRBNB_PASSW_SECRET']

website = "https://www.airbnb.com/performance/conversion/conversion_rate"

# Set up Chrome WebDriver with more stealth options
options = webdriver.ChromeOptions()
options.add_argument("--disable-blink-features=AutomationControlled")
options.add_argument("--disable-dev-shm-usage")
options.add_argument("--no-sandbox")
options.add_argument("--window-size=1920x1080")
options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36")

# Prevent detection of automation tools
options.add_experimental_option("excludeSwitches", ["enable-automation"])
options.add_experimental_option('useAutomationExtension', False)

# Path to the ChromeDriver
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

# Stealth Script to prevent detection
driver.execute_cdp_cmd('Page.addScriptToEvaluateOnNewDocument', {
    'source': '''
        Object.defineProperty(navigator, 'webdriver', {
            get: () => undefined
        });
    '''
})

driver.get(website)

# Using the Login to Enter the Airbnb websites first so the data becomes available
log = driver.find_element(By.XPATH, """//button[@aria-label="Continue with email"]""")
log.click()
driver.find_element(By.XPATH, """//input[@inputmode="email"]""").send_keys(username)
time.sleep(2)
log1 = driver.find_element(By.XPATH, """//button[@data-testid="signup-login-submit-btn"]""")
log1.click()
time.sleep(2)
driver.find_element(By.XPATH, """//input[@name="user[password]"]""").send_keys(passw)
time.sleep(2)
log1 = driver.find_element(By.XPATH, """//button[@data-testid="signup-login-submit-btn"]""")
log1.click()
