from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import os
import json
from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build

# Google Sheets setup
SHEET_ID = '1S6gAIsjuYyGtOmWFGpF9okAPMWq6SnZ1zbIylBZqCt4'
SHEET_NAME1 = 'Airbnb_Metrics'  # Sheet to clear data below header and write new data

username = os.environ['AIRBNB_USER_SECRET']
passw = os.environ['AIRBNB_PASSW_SECRET']
website = "https://www.airbnb.com/performance/conversion/conversion_rate"

# Get Google Sheets credentials from environment variable
GOOGLE_SHEETS_CREDENTIALS = os.getenv("GOOGLE_SHEETS_CREDENTIALS")
credentials = Credentials.from_service_account_info(json.loads(GOOGLE_SHEETS_CREDENTIALS))

# Create Google Sheets API service
service = build("sheets", "v4", credentials=credentials)

# Set up Chrome WebDriver
options = webdriver.ChromeOptions()
options.add_argument("--headless")
options.add_argument("--disable-dev-shm-usage")
options.add_argument("--no-sandbox")
options.add_argument("--disable-gpu")
options.add_argument("--window-size=1920x1080")
options.add_argument("--remote-debugging-port=9222")

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

# Wait for the login button to be clickable and click it
wait = WebDriverWait(driver, 20)
log = wait.until(EC.element_to_be_clickable((By.XPATH, """//button[@aria-label="Continue with email"]""")))
log.click()

# Enter username
wait.until(EC.presence_of_element_located((By.XPATH, """//input[@inputmode="email"]"""))).send_keys(username)
time.sleep(2)

# Submit username and enter password
log1 = driver.find_element(By.XPATH, """//button[@data-testid="signup-login-submit-btn"]""")
log1.click()
time.sleep(2)
wait.until(EC.presence_of_element_located((By.XPATH, """//input[@name="user[password]"]"""))).send_keys(passw)
time.sleep(2)
log1 = driver.find_element(By.XPATH, """//button[@data-testid="signup-login-submit-btn"]""")
log1.click()

# Wait for the page to load after logging in
time.sleep(10)
driver.get(website)
html_content = driver.page_source
print(html_content)
time.sleep(10)

# Method of getting the listing numbers available on the website
time.sleep(3)
all_listing = wait.until(EC.element_to_be_clickable((By.XPATH, """//div[@data-testid="listingPicker"]/button""")))
all_listing.click()

time.sleep(2)
lists = wait.until(EC.presence_of_all_elements_located((By.XPATH, """//div[@class="_1a8jl99"]/div/div[1]""")))

Listings = []
for list_item in lists:
    div_id = list_item.get_attribute('id')
    Listings.append(div_id)

print(Listings)
