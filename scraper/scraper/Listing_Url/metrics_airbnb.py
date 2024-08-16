import os
import time
import datetime
import undetected_chromedriver as uc
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

start_time = time.time()

username = os.environ['AIRBNB_USER_SECRET']
passw = os.environ['AIRBNB_PASSW_SECRET']

website = "https://www.airbnb.com/performance/conversion/conversion_rate"

# Set up undetected Chrome WebDriver
options = uc.ChromeOptions()
options.add_argument("--disable-blink-features=AutomationControlled")
options.add_argument("--disable-dev-shm-usage")
options.add_argument("--no-sandbox")
options.add_argument("--window-size=1920x1080")
options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36")

driver = uc.Chrome(options=options)

driver.get(website)

# Using the Login to Enter the Airbnb websites first so the data becomes available
log = WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, """//button[@aria-label="Continue with email"]""")))
log.click()

email_field = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, """//input[@inputmode="email"]""")))
email_field.send_keys(username)
time.sleep(2)

log1 = WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, """//button[@data-testid="signup-login-submit-btn"]""")))
log1.click()
time.sleep(2)

password_field = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, """//input[@name="user[password]"]""")))
password_field.send_keys(passw)
time.sleep(2)

log1 = WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, """//button[@data-testid="signup-login-submit-btn"]""")))
log1.click()

# Method of getting the listing numbers available on the website
try:
    all_listing = WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, """//div[@data-testid="listingPicker"]/button""")))
    all_listing.click()
except TimeoutException:
    print("Element not found or not clickable")

time.sleep(2)

lists = WebDriverWait(driver, 20).until(EC.presence_of_all_elements_located((By.XPATH, """//div[@class='_1a8jl99']/div/div[1]""")))

Listings = []
for list_item in lists:
    div_id = list_item.get_attribute('id')
    Listings.append(div_id)

print("Listings found:", Listings)
