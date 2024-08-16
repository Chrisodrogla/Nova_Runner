import os
import time
from requests_html import HTMLSession

# Get credentials from environment variables
username = os.environ['AIRBNB_USER_SECRET']
passw = os.environ['AIRBNB_PASSW_SECRET']

website = "https://www.airbnb.com/performance/conversion/conversion_rate"

# Initialize an HTML session
session = HTMLSession()

# Get the login page
response = session.get(website)
response.html.render(sleep=2)  # Renders the JavaScript on the page

# Find and click the "Continue with email" button
continue_email_btn = response.html.xpath("//button[@aria-label='Continue with email']", first=True)
if continue_email_btn:
    continue_email_btn.click()

# Enter the email
email_input = response.html.xpath("//input[@inputmode='email']", first=True)
if email_input:
    email_input.send_keys(username)
    time.sleep(2)

# Click the submit button after entering the email
submit_btn = response.html.xpath("//button[@data-testid='signup-login-submit-btn']", first=True)
if submit_btn:
    submit_btn.click()
    time.sleep(2)

# Enter the password
password_input = response.html.xpath("//input[@name='user[password]']", first=True)
if password_input:
    password_input.send_keys(passw)
    time.sleep(2)

# Click the submit button after entering the password
submit_btn = response.html.xpath("//button[@data-testid='signup-login-submit-btn']", first=True)
if submit_btn:
    submit_btn.click()

# After logging in, you can access the content on the desired page
time.sleep(2)
performance_page = session.get(website)
performance_page.html.render(sleep=2)

# Extract the data you need
# For example, extracting a metric
conversion_rate = performance_page.html.xpath("//span[contains(@class,'conversion-rate')]", first=True)
if conversion_rate:
    print("Conversion Rate:", conversion_rate.text)
else:
    print("Conversion Rate data not found.")
