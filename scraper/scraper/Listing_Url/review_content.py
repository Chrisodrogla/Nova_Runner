import pandas as pd
from datetime import date
import time
from selenium import webdriver
from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import os
import json

# Set up Chrome WebDriver with custom options
options = webdriver.ChromeOptions()
options.add_argument("--headless")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")
options.add_argument("--disable-gpu")
options.add_argument("--window-size=1920x1080")
options.add_argument("--display=:99")  # Set display to Xvfb

# Google Sheets setup
SHEET_ID = '1RG-5uy_k3GbpDYINKDAZLh0UomU3U41N-Pk50Qtaus8'
SHEET_NAME1 = 'Reviews'  # Sheet to clear data below header and write new data

# Get Google Sheets credentials from environment variable
GOOGLE_SHEETS_CREDENTIALS = os.getenv("GOOGLE_SHEETS_CREDENTIALS")
credentials = Credentials.from_service_account_info(json.loads(GOOGLE_SHEETS_CREDENTIALS))

# Create Google Sheets API service
service = build("sheets", "v4", credentials=credentials)

link_websites1 = [
    "https://www.airbnb.com/rooms/7146166",
    "https://www.airbnb.com/rooms/796474546246084466",
    "https://www.airbnb.com/rooms/37941371",

    # Add more URLs as needed
]

DateToday = date.today()
UpdatedAt = DateToday.strftime("%Y-%m-%d")

reviews_data = []
data = []

for website in link_websites1:
    revweb = website + "/reviews?"
    driver = webdriver.Chrome(options=options)
    listing_id = website.split('/')[-1]
    driver.get(revweb)

    time.sleep(5)  # Wait for the page to load

    All_Reviews2 = driver.find_elements("xpath", """//div[@class="r1are2x1 atm_gq_1vi7ecw dir dir-ltr"]""")

    if All_Reviews2:

        # Locate the scrollable element, this needs to be the correct XPath for the reviews container
        try:
            scrollable_div = driver.find_element("xpath", '//div[@class="_17itzz4"]')
        except Exception as e:
            print(f"Could not locate scrollable element: {e}")
            driver.quit()
            continue

        # Scroll down until all reviews are loaded
        last_height = driver.execute_script("return arguments[0].scrollHeight;", scrollable_div)
        while True:
            # Scroll down
            driver.execute_script("arguments[0].scrollTo(0, arguments[0].scrollHeight);", scrollable_div)

            # Wait for reviews to load
            time.sleep(3)

            # Calculate new scroll height and compare with last scroll height
            new_height = driver.execute_script("return arguments[0].scrollHeight;", scrollable_div)
            if new_height == last_height:
                break
            last_height = new_height

        All_Reviews = driver.find_elements("xpath", """//div[@class="r1are2x1 atm_gq_1vi7ecw dir dir-ltr"]""")

        for review in All_Reviews:

            name_element = review.find_element("xpath", ".//h2[@elementtiming='LCP-target']")
            name = name_element.text.strip()

            # Extract the date of review
            date_element = review.find_element("xpath",
                                               """.//div[contains(@class, "s78n3tv ")]""").text.split(
                '·')[1]
            date_review = date_element.strip().strip('\n,')

            # Extract the star rating
            star_element = review.find_element("xpath", ".//span[contains(text(), 'Rating,')]")
            star_review = star_element.text.strip().strip('Rating, ')

            Stayedat = ''

            content_element = review.find_element("xpath",
                                                  ".//div[@class='r1bctolv atm_c8_1sjzizj atm_g3_1dgusqm atm_26_lfmit2_13uojos atm_5j_1y44olf_13uojos atm_l8_1s2714j_13uojos dir dir-ltr']")
            content_review = content_element.text.strip()

            try:  # Extract the response content
                response_element = review.find_element("xpath",
                                                       ".//div[@data-testid='pdp-reviews-response']//div[contains(@style, 'line-height: 1.25rem')]")
                response_content = response_element.text.strip()
            except:

                response_content = ''

            try:  # Extract the response date
                response_date_element = review.find_element("xpath",
                                                            ".//div[@data-testid='pdp-reviews-response']//div[@class='s15w4qkt atm_c8_1w0928g atm_g3_1dd5bz5 atm_cs_6adqpa atm_7l_1wzk1hz dir dir-ltr']")
                response_date = response_date_element.text.strip()
            except:

                response_date = ''

                # Append the extracted data to the list
            reviews_data.append({
                "Listing ID": listing_id,
                'name': name,
                'date_review': date_review,
                'star_review': star_review,
                'Stayedat': Stayedat,
                'content_review': content_review,
                'response_content': response_content,
                'response_date': response_date,
                'UpdatedAt': UpdatedAt
            })

    else:
        name = 'Listing has no Review Content or Unavailable'
        date_review = ''
        star_review = ''
        Stayedat = ''
        content_review = ''
        response_content = ''
        response_date = ''

        # Append the extracted data to the list
        reviews_data.append({
            "Listing ID": listing_id,
            'name': name,
            'date_review': date_review,
            'star_review': star_review,
            'Stayedat': Stayedat,
            'content_review': content_review,
            'response_content': response_content,
            'response_date': response_date,
            'UpdatedAt': UpdatedAt
        })

df = pd.DataFrame(reviews_data)

# Clear all data below header in the "Review" sheet
service.spreadsheets().values().clear(
    spreadsheetId=SHEET_ID,
    range=f"{SHEET_NAME1}!A2:Z"
).execute()

# Write new data to the "Review" sheet starting from row 2
service.spreadsheets().values().update(
    spreadsheetId=SHEET_ID,
    range=f"{SHEET_NAME1}!A2",
    valueInputOption="RAW",
    body={"values": df.values.tolist()}
).execute()
