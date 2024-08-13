import os
import time
import datetime
from selenium import webdriver
import shutil
import json
from selenium.common.exceptions import NoSuchElementException
from google.oauth2.service_account import Credentials
import pytz
import pandas as pd
from datetime import datetime, timedelta
import calendar

start_time = time.time()

username = os.environ['AIRBNB_USER_SECRET']
passw = os.environ['AIRBNB_PASSW_SECRET']

website = "https://www.airbnb.com/performance/conversion/conversion_rate"

# Google Sheets setup
SHEET_ID = '1S6gAIsjuYyGtOmWFGpF9okAPMWq6SnZ1zbIylBZqCt4'
SHEET_NAME1 = 'Airbnb_Metrics'  # Sheet to clear data below header and write new data

# Get Google Sheets credentials from environment variable
GOOGLE_SHEETS_CREDENTIALS = os.getenv("GOOGLE_SHEETS_CREDENTIALS")
credentials = Credentials.from_service_account_info(json.loads(GOOGLE_SHEETS_CREDENTIALS))

# Set up Chrome WebDriver
options = webdriver.ChromeOptions()
options.add_argument("--headless")
options.add_argument("--disable-dev-shm-usage")
options.add_argument("--no-sandbox")


driver = webdriver.Chrome(options=options)
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

# MEthod of getting the listing numbers available on the website
time.sleep(3)
all_listing = driver.find_element("xpath", """//div[@data-testid="listingPicker"]/button""")
all_listing.click()
time.sleep(2)
lists = driver.find_elements("xpath", """//div[@class="_1a8jl99"]/div/div[1]""")
Listings = []
for list_item in lists:
    div_id = list_item.get_attribute('id')
    Listings.append(div_id)

# Scrape the Date_basis from a web element
Date_basis = driver.find_element("xpath", """//div[@class="_x4llbi"]""").text.split(': ')[1]

# Parse the Date_basis to extract the month and day
month_day = Date_basis.split()
month_str = month_day[0]
day = int(month_day[1])

# Convert the month from the string to a number
month_num = datetime.strptime(month_str, "%b").month

# Determine the current year and adjust if the month is ahead of the current month
current_year = datetime.now().year
if month_num > datetime.now().month:
    current_year += 1

# Calculate the base date (Date_basis)
base_date = datetime(year=current_year, month=month_num, day=day)

# Define number of months to go back and forward
months_back = 1  # Change this value as needed for past months
months_forward = 1  # Change this value as needed for future months

# Generate URLs for past months
Listing_Urls = []

for i in range(-months_back, months_forward + 1):
    # Calculate the start and end dates for the months relative to Date_basis
    adjusted_base_date = base_date + timedelta(days=calendar.monthrange(base_date.year, base_date.month)[1] * i)
    start_date = adjusted_base_date.replace(day=1)
    end_date = start_date.replace(day=calendar.monthrange(start_date.year, start_date.month)[1])

    # Calculate relative day offsets from Date_basis
    start_value = f"-{(base_date - start_date).days}"
    end_value = f"-{(base_date - end_date).days}"

    # Generate URL for each listing
    for Listing in Listings:
        Listing_Urls.append({
            "Listing_Url": f"https://www.airbnb.com/performance/conversion/conversion_rate?lid%5B%5D={Listing}&ctype=MARKET&ds-start={start_value}&ds-end={end_value}",
            "ListingID": Listing,
            "StartDate": start_date.strftime('%Y-%m-%d'),
            "EndDate": end_date.strftime('%Y-%m-%d')
        })

time.sleep(3)

# Initialize an empty list to store the results
results = []
for listing in Listing_Urls:
    driver.get(listing['Listing_Url'])
    time.sleep(3)
    Tabs = driver.find_elements("xpath", """//ul[@class="_1r7lmfk2"]/li""")
    Market = driver.find_element("xpath", """//option[@value="MARKET"]""").click()
    time.sleep(2)
    # Scrape for B_Conversions or Booking Conversion

    B_Conversions = driver.find_elements("xpath", """//div[@class="_1gerx23"]/button/div[1]""")
    Overall = driver.find_element("xpath", """//div[@class="_c899vt"]""").text.split("listings is ")[1].split(" than")[
        0] if "listings is " in driver.find_element("xpath", """//div[@class="_c899vt"]""").text else "No Data"
    OverallConversionRate = B_Conversions[0].text.strip('%') if B_Conversions[0].text != '-' else '0'
    FPImpressionRate = B_Conversions[1].text.strip('%') if B_Conversions[1].text != '-' else '0'
    ClickThroughRate = B_Conversions[2].text.strip('%') if B_Conversions[2].text != '-' else '0'
    ViewtoBookRate = B_Conversions[3].text.strip('%') if B_Conversions[3].text != '-' else '0'
    OverallValue = float(Overall.split(' ')[0].strip('%')) if Overall != "No Data" else "No Data"
    OverallConversionRate_comp = (
        f"{float(OverallConversionRate.strip('%')) + (0 if OverallValue == 'No Data' else OverallValue)}%" if "lower" in Overall else f"{float(OverallConversionRate.strip('%')) - (0 if OverallValue == 'No Data' else OverallValue)}").strip(
        '%')

    time.sleep(2)
    lead_time_url = listing['Listing_Url'].replace('conversion_rate?', 'booking_window?')
    driver.get(lead_time_url)
    #     To_B_lead_time_Tab = Tabs[1].click()
    time.sleep(2)
    B_Lead_times = driver.find_elements("xpath", """//div[@class="_1gerx23"]/button/div[1]""")
    LeadingComp = \
    driver.find_element("xpath", """//div[@class="_c899vt"]""").text.split("listings is ")[1].split(" than")[
        0] if "listings is " in driver.find_element("xpath", """//div[@class="_c899vt"]""").text else "No Data"
    LeadingTime = B_Lead_times[0].text.split(' ')[0] if B_Lead_times[0].text.split(' ')[0] != '-' else '0'
    ValueLeadingComp = float(LeadingComp.split(' ')[0]) if LeadingComp != "No Data" else "No Data"
    LeadingTime_comp = float(LeadingTime) + (
        0 if ValueLeadingComp == 'No Data' else ValueLeadingComp) if "lower" in LeadingComp else float(LeadingTime) - (
        0 if ValueLeadingComp == 'No Data' else ValueLeadingComp)

    # Scrape for Views Tab

    time.sleep(2)
    view_url = listing['Listing_Url'].replace('conversion_rate?', 'p3_impressions?')
    driver.get(view_url)
    #    To_Views_Tab = Tabs[3].click()
    time.sleep(2)
    Views = driver.find_elements("xpath", """//div[@class="_1gerx23"]/button/div[1]""")
    PageView = driver.find_element("xpath", """//div[@class="_c899vt"]""").text.split("listings is ")[1].split(" than")[
        0] if "listings is " in driver.find_element("xpath", """//div[@class="_c899vt"]""").text else "No Data"
    TotalPageView = Views[0].text if Views[0].text != '-' else '0'
    FPImpression = Views[1].text if Views[1].text != '-' else '0'
    PageViewValue = int(PageView.split(' ')[0]) if PageView != "No Data" else "No Data"
    TotalPageView_comp = int(TotalPageView) + (
        0 if PageViewValue == 'No Data' else PageViewValue) if "lower" in PageView else int(TotalPageView) - (
        0 if PageViewValue == 'No Data' else PageViewValue)
    # Scrape for Wishlist Additions Tab

    time.sleep(2)
    wish_url = listing['Listing_Url'].replace('conversion_rate?', 'wishlist?')
    driver.get(wish_url)
    #     To_Wish_Tab = Tabs[4].click()
    time.sleep(2)
    Wishlist = driver.find_elements("xpath", """//div[@class="_1gerx23"]/button/div[1]""")
    Additions_comp = \
    driver.find_element("xpath", """//div[@class="_c899vt"]""").text.split("listings is ")[1].split(" than")[
        0] if "listings is " in driver.find_element("xpath", """//div[@class="_c899vt"]""").text else "No Data"
    WishlistAdditions = Wishlist[0].text if Wishlist[0].text != '-' else '0'
    AdditionsValue = int(Additions_comp.split(' ')[0]) if Additions_comp != "No Data" else "No Data"

    WishlistAdditions_comp = int(WishlistAdditions) + (
        0 if AdditionsValue == 'No Data' else AdditionsValue) if "lower" in Additions_comp else int(
        WishlistAdditions) - (0 if AdditionsValue == 'No Data' else AdditionsValue)

    # Append the results to the list
    results.append({
        'ListingID': listing['ListingID'],
        'StartDate': listing['StartDate'],
        'EndDate': listing['EndDate'],
        'FPImpression': FPImpression,
        'TotalPageView': TotalPageView,
        'TotalPageView_comp': TotalPageView_comp,
        'FPImpressionRate': FPImpressionRate,
        'ClickThroughRate': ClickThroughRate,
        'ViewtoBookRate': ViewtoBookRate,
        'OverallConversionRate': OverallConversionRate,
        'OverallConversionRate_comp': OverallConversionRate_comp,
        'LeadingTime': LeadingTime,
        'LeadingTime_comp': LeadingTime_comp,
        'WishlistAdditions': WishlistAdditions,
        'WishlistAdditions_comp': WishlistAdditions_comp
    })

# Create a DataFrame from the results
df = pd.DataFrame(results)

# Record the end time
end_time = time.time()

# Calculate the elapsed time
elapsed_time = end_time - start_time
minutes = int(elapsed_time // 60)
seconds = int(elapsed_time % 60)

print(f"Time takes {minutes} minutes and {seconds} seconds")

service.spreadsheets().values().clear(
    spreadsheetId=SHEET_ID,
    range=f"{SHEET_NAME1}!A2:Z"
).execute()

# Write new data to the 'Airbnb_Metrics' sheet starting from row 2
service.spreadsheets().values().update(
    spreadsheetId=SHEET_ID,
    range=f"{SHEET_NAME1}!A2",
    valueInputOption="RAW",
    body={"values": df.values.tolist()}
).execute()