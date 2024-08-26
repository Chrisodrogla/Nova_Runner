import os
import time
import datetime
import shutil
import json
import re
import pandas as pd
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from bs4 import BeautifulSoup


# Get environment variables for username and password
username = os.getenv("USERNAME1")
password = os.getenv("PASSWORD1")

# Airbnb URL
website = "https://www.airbnb.com/hosting/reservations/completed"

# Set up Chrome WebDriver with options
options = webdriver.ChromeOptions()
# options.add_argument("--headless")  # Uncomment if you want to run headless
options.add_argument("--disable-dev-shm-usage")
options.add_argument("--no-sandbox")
# options.add_argument("--disable-gpu")  # Uncomment if you want to disable GPU
options.add_argument("--start-maximized")

driver = webdriver.Chrome(options=options)
driver.get(website)

# Log in to Airbnb
driver.find_element("xpath", """//button[@aria-label="Continue with email"]""").click()
time.sleep(2)
driver.find_element("xpath", """//input[@inputmode="email"]""").send_keys(username)
time.sleep(2)
driver.find_element("xpath", """//button[@data-testid="signup-login-submit-btn"]""").click()
time.sleep(2)
driver.find_element("xpath", """//input[@name="user[password]"]""").send_keys(password)
time.sleep(2)
driver.find_element("xpath", """//button[@data-testid="signup-login-submit-btn"]""").click()
time.sleep(6)

# Initialize an empty list to store all data across pages
all_data = []

while True:
    # Find all the rows in the table
    rows = driver.find_elements("xpath", """//table/tbody/tr""")
    data = []

    # Loop through each row and extract the text for each cell, Contact, and GuestLink
    for row in rows:
        columns = row.find_elements("xpath", ".//td")
        row_data = [col.text for col in columns]

        # Extract Contact
        guest_contact = (
            row.find_element("xpath", ".//td[@class='_1keevci4']").get_attribute("innerText")
            if row.find_elements("xpath", ".//td[@class='_1keevci4']")
            else None
        )
        row_data.append(guest_contact)

        # Extract GuestLink
        guest_link_element = row.find_elements("xpath", ".//span[@class='_e296pg']/a")
        guest_link = guest_link_element[0].get_attribute("href") if guest_link_element else None
        row_data.append(guest_link)

        data.append(row_data)

    # Append this page's data to the overall data list
    all_data.extend(data)

    try:
        # Try to find the "Next" button and click it
        next_button = driver.find_element(
            "xpath", """//button[@aria-label="Next" and not(@disabled) and @type="button"]"""
        )
        next_button.click()
        time.sleep(2)  # Add a small delay to allow the next page to load
    except NoSuchElementException:
        break  # Break the loop if the "Next" button is not found

# Create a DataFrame from the extracted data
column_names = [f"column{i + 1}" for i in range(len(all_data[0]) - 2)] + ['Contact', 'GuestLink']
df = pd.DataFrame(all_data, columns=column_names)

# Process the DataFrame
df['column2'] = df['column2'].apply(lambda x: x.split('/')[0] if pd.notna(x) else None)

# Convert the relevant date columns to MM/DD/YYYY format
date_columns = ['column4', 'column5']
for col in date_columns:
    df[col] = pd.to_datetime(df[col].str.split('\n').str[0]).dt.strftime('%m/%d/%Y')

def extract_guests(guest_info):
    if pd.notna(guest_info):
        adults = re.search(r'(\d+)\s*adults?', guest_info, re.IGNORECASE)
        children = re.search(r'(\d+)\s*(children?|child)', guest_info, re.IGNORECASE)
        infants = re.search(r'(\d+)\s*infants?', guest_info, re.IGNORECASE)

        return {
            '# of adults': int(adults.group(1)) if adults else 0,
            '# of children': int(children.group(1)) if children else 0,
            '# of infants': int(infants.group(1)) if infants else 0,
        }
    return {'# of adults': 0, '# of children': 0, '# of infants': 0}

# Apply the extraction function and expand into new columns
guest_info_df = df['column2'].apply(extract_guests).apply(pd.Series)

# Add the extracted guest info to the DataFrame
df = pd.concat([df, guest_info_df], axis=1)

# Split the 'Booked' column into 'BookedDate' and 'BookedTime'
df[['BookedDate', 'BookedTime']] = df['column6'].str.split('\n', expand=True)
df['BookedDate'] = pd.to_datetime(df['BookedDate']).dt.strftime('%m/%d/%Y')

# Rename columns and remove specific columns
df.rename(columns={
    'column1': 'Status',
    'column2': 'GuestName',
    'column4': 'CheckIn',
    'column5': 'CheckOut',
    'BookedDate': 'Booked',
    'column7': 'Listing',
    'column8': 'ConfirmationCode',
    'column9': 'Earnings'
}, inplace=True)
df.drop(columns=['column3', 'column6', 'column10'], inplace=True)

# Function to extract review from a URL
def get_review(confirmation_code):
    url = f"https://www.airbnb.com/hosting/reservations/details/{confirmation_code}"
    driver.get(url)
    time.sleep(2)  # Wait for the page to load fully

    # Parse the page with BeautifulSoup
    soup = BeautifulSoup(driver.page_source, 'html.parser')

    # Extract the review if it exists
    review_div = soup.find('div', {'class': 'bvrobmf dir dir-ltr'})
    return review_div.text if review_div else None

# Add the Review column to the DataFrame
df['Review'] = df['ConfirmationCode'].apply(get_review)

# Save the modified DataFrame as JSON
output_dir = r'C:\Users\calgo\PycharmProjects\pythonProject\Nova_Runner\scraper\scraper\Listing_Url\output'
output_file = 'ReservationReview.json'
os.makedirs(output_dir, exist_ok=True)
output_path = os.path.join(output_dir, output_file)

df.to_json(output_path, orient='records', indent=4)
