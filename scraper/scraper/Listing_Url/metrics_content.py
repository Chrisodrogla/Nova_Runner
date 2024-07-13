import os
import time
import datetime
import pytz
import json
from selenium import webdriver
from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build

# Google Sheets setup
SHEET_ID = '10OgYeu7oj5Lwtr4gGy14zXuZlAk0gibSbgq_AmUtf7Q'
SHEET_DATA = 'rankbrz_Data'
SHEET_IMPRESSIONS = 'rankbrz_impressions'
SHEET_CLICK_THROUGHS = 'rankbrz_click'
SHEET_LISTING_VIEWS = 'rankbrz_listing_v'
SHEET_CONVERSION_RATE = 'rankbrz_conversion_r'
SHEET_LEAD_TIMES = 'rankbrz_lead_times'
SHEET_AIRBNB_OCCUPANCY = 'rankbrz_abnb_occu'
SHEET_AVG_DAILY_RATES = 'rankbrz_daily_rates'
SHEET_REVENUE = 'rankbrz_revenue'
# JSON_FILE_PATH = "scraper/scraper/Listing_Url/json_file/listing_attribute.json"
# Get Google Sheets credentials from environment variable
GOOGLE_SHEETS_CREDENTIALS = os.getenv("GOOGLE_SHEETS_CREDENTIALS")
credentials = Credentials.from_service_account_info(json.loads(GOOGLE_SHEETS_CREDENTIALS))

# Create Google Sheets API service
service = build("sheets", "v4", credentials=credentials)

eastern_tz = pytz.timezone("America/New_York")
current_time = datetime.datetime.now(eastern_tz)

username = os.environ['RANKB_USERNAME_SECRET']
passw = os.environ['RANKB_PASSWORD_SECRET']
website = "https://app.rankbreeze.com/listings"

# Set up Chrome WebDriver
options = webdriver.ChromeOptions()
options.add_argument("--headless")
options.add_argument("--disable-dev-shm-usage")
options.add_argument("--no-sandbox")

driver = webdriver.Chrome(options=options)
driver.get(website)

time.sleep(2)

driver.find_element("xpath", """(//div[@class="form-group"]/input)[1]""").send_keys(username)
time.sleep(2)
driver.find_element("xpath", """(//div[@class="form-group"]/input)[2]""").send_keys(passw)
log = driver.find_element("xpath", """(//div[@class="form-group"]/input)[3]""")
time.sleep(2)
log.click()
time.sleep(3)


#
# # Read JSON data from local file
# with open(JSON_FILE_PATH, 'r') as file:

# driver.get(website)
#
# time.sleep(2)

# driver.find_element("xpath", """(//div[@class="form-group"]/input)[1]""").send_keys(username)
# time.sleep(2)
# driver.find_element("xpath", """(//div[@class="form-group"]/input)[2]""").send_keys(passw)
# log = driver.find_element("xpath", """(//div[@class="form-group"]/input)[3]""")
# time.sleep(2)
# log.click()
# time.sleep(20)

proxy_links = []

while True:
    # Get all the desired links on the current page
    links = driver.find_elements("xpath", """//a[@class="btn btn-outline-primary card-btn custom-nav-button mr-1"]""")
    for link in links:
        web = link.get_attribute("href")
        proxy_links.append(web)

    time.sleep(10)
    # Check if there's a "Next" button on the page
    next_buttons = driver.find_elements("xpath", """//span[@class="next"]""")
    if len(next_buttons) > 0:
        # Click the first "Next" button
        next_buttons[0].click()
    else:

        links = driver.find_elements("xpath",
                                     """//a[@class="btn btn-outline-primary card-btn custom-nav-button mr-1"]""")
        for link in links:
            web = link.get_attribute("href")
            proxy_links.append(web)
        # No "Next" button, exit the loop
        break






















# proxy_links = [
#     "https://app.rankbreeze.com/rankings/73635",
#     "https://app.rankbreeze.com/rankings/73636",
#
# ]

data = []
overall_impressions = []
overall_click_throughs = []
overall_listing_views = []
overall_conversion_rate = []
overall_lead_times = []
overall_airbnb_occupancy = []
overall_avg_daily_rates = []
overall_revenue = []

for website in proxy_links:
    driver.get(website)
    time.sleep(2)

    link = website
    link_Id = website.strip("https://app.rankbreeze.com/rankings/")

    proxy_title = driver.find_element("xpath", """//*[@id="get-email"]/div/main/div[3]/div[1]/h2""").get_attribute("innerText")

    guest_satisfaction = driver.find_element("xpath", """(//div[@class="single-value"]/b)""").get_attribute("innerText")
    reviews_count = driver.find_element("xpath", """(//div[@class="single-value"]/b)[2]|(//div[@class="single-value"]/b)""").get_attribute("innerText")

    date_str = current_time.strftime("%Y-%m-%d")
    date_hours_str = current_time.strftime("%Y-%m-%d %H:%M:%S")

    def extract_table_data(rows, num_columns):
        table_data = []
        for row in rows:
            columns = row.find_elements("xpath", "./td")
            if len(columns) >= num_columns:
                column_texts = [column.get_attribute("innerText").strip() for column in columns[:num_columns]]
                if constant_values:
                    column_texts.extend(constant_values)
                table_data.append(tuple(column_texts))
        return table_data

    impressions = driver.find_elements("xpath", """//*[@id="first_page_search_impressions"]//tbody/tr""")
    search_conversion_rate = driver.find_elements("xpath", """//*[@id="search_conversion_rate"]//tbody/tr""")
    listing_views = driver.find_elements("xpath", """//*[@id="page_views"]//tbody/tr""")
    conversion_rate = driver.find_elements("xpath", """//*[@id="conversion_rate"]//tbody/tr""")
    lead_times = driver.find_elements("xpath", """//*[@id="booking_lead_time"]//tbody/tr""")
    airbnb_occupancy = driver.find_elements("xpath", """//*[@id="occupancy_rate"]//tbody/tr""")
    avg_daily_rates = driver.find_elements("xpath", """//*[@id="average_daily_rate"]//tbody/tr""")
    revenue = driver.find_elements("xpath", """//*[@id="revenue"]//tbody/tr""")

    constant_values = [link, link_Id, proxy_title, date_str, date_hours_str]

    overall_impressions.extend(extract_table_data(impressions, 3))
    overall_click_throughs.extend(extract_table_data(search_conversion_rate, 3))
    overall_listing_views.extend(extract_table_data(listing_views, 3))
    overall_conversion_rate.extend(extract_table_data(conversion_rate, 3))
    overall_lead_times.extend(extract_table_data(lead_times, 3))
    overall_airbnb_occupancy.extend(extract_table_data(airbnb_occupancy, 3))
    overall_avg_daily_rates.extend(extract_table_data(avg_daily_rates, 3))
    overall_revenue.extend(extract_table_data(revenue, 2))

    data.append({
        "Link": link,
        "Link Id": link_Id,
        "Rental Name": proxy_title,
        "Reviews Count": guest_satisfaction,
        "Star Reviews": reviews_count,
        "Date Gathered": date_str,
        "Date Gathered Hours": date_hours_str,
    })

driver.quit()

overall_impressions = [(item[0], item[1].replace("impressions", "").replace(",", "").strip(),
                        item[2].replace("impressions", "").replace(",", "").strip(), *item[3:]) for item in
                       overall_impressions]

overall_click_throughs = [(item[0], item[1].replace("%", "").strip(), item[2].replace("%", "").strip(), *item[3:]) for
                          item in overall_click_throughs]

overall_listing_views = [(item[0], item[1].replace("views", "").replace(",", "").strip(),
                          item[2].replace("views", "").replace(",", "").strip(), *item[3:]) for item in
                         overall_listing_views]

overall_conversion_rate = [(item[0], item[1].replace("%", "").strip(), item[2].replace("%", "").strip(), *item[3:]) for
                           item in overall_conversion_rate]

overall_lead_times = [(item[0], item[1].replace("days", "").replace(",", "").strip(),
                       item[2].replace("days", "").replace(",", "").strip(), *item[3:]) for item in overall_lead_times]

overall_airbnb_occupancy = [(item[0], item[1].replace("%", "").replace(",", "").strip(),
                             item[2].replace("%", "").strip(), *item[3:]) for item in
                            overall_airbnb_occupancy]

overall_avg_daily_rates = [(item[0], item[1].replace("$", "").replace(",", "").strip(),
                            item[2].replace("$", "").replace(",", "").strip(), *item[3:]) for item in
                           overall_avg_daily_rates]

overall_revenue = [(item[0], item[1].replace("$", "").replace(",", "").strip(), *item[2:]) for item in overall_revenue]

# Function to update Google Sheets
def update_google_sheet(sheet_id, sheet_name, data):
    # Clear existing data in the sheet
    service.spreadsheets().values().clear(
        spreadsheetId=sheet_id,
        range=f"{sheet_name}!A2:Z",
    ).execute()

    # Append new data
    service.spreadsheets().values().append(
        spreadsheetId=sheet_id,
        range=f"{sheet_name}!A2",
        valueInputOption="RAW",
        body={"values": data},
    ).execute()

# Convert data to list of lists for Google Sheets
data_list = [[item['Link'], item['Link Id'], item['Rental Name'], item['Reviews Count'], item['Star Reviews'],
              item['Date Gathered'], item['Date Gathered Hours']] for item in data]

# Update Google Sheets with each dataset
update_google_sheet(SHEET_ID, SHEET_DATA, data_list)
update_google_sheet(SHEET_ID, SHEET_IMPRESSIONS, overall_impressions)
update_google_sheet(SHEET_ID, SHEET_CLICK_THROUGHS, overall_click_throughs)
update_google_sheet(SHEET_ID, SHEET_LISTING_VIEWS, overall_listing_views)
update_google_sheet(SHEET_ID, SHEET_CONVERSION_RATE, overall_conversion_rate)
update_google_sheet(SHEET_ID, SHEET_LEAD_TIMES, overall_lead_times)
update_google_sheet(SHEET_ID, SHEET_AIRBNB_OCCUPANCY, overall_airbnb_occupancy)
update_google_sheet(SHEET_ID, SHEET_AVG_DAILY_RATES, overall_avg_daily_rates)
update_google_sheet(SHEET_ID, SHEET_REVENUE, overall_revenue)




