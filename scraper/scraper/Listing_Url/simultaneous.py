import json
import csv
import sys
import time
import os
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from gspread_dataframe import set_with_dataframe
import pandas as pd

sys.path.insert(0, os.path.join(os.getcwd(), "scraper"))
import concurrent.futures
from scraper.strategies.airbnb_com.search_page import AirbnbComSearchStrategy
import logging

batch_id = os.getenv('BATCH_ID', 'Batch1')
start_time = time.time()

with open('scraper/scraper/Listing_Url/json_file/final_rental_link.json', 'r') as f:
    data = json.load(f)
    rental_links = data[batch_id]

def filter_results(result, needed_keys):
    filtered_results = []
    for listing in result:
        for item in listing:
            filtered_result = {key: item.get(key, None) for key in needed_keys}
            filtered_results.append(filtered_result)
    return filtered_results

def scrape_rental(rental, scraper, needed_keys):
    config = {"url": rental["listing_link_format"]}
    result = scraper.execute(config)
    filtered_results = filter_results(result, needed_keys)
    final_results = []
    for filtered_result in filtered_results:
        final_result = {
            # "rankbreeze_Id": rental["rankbreeze_Id"],
            "rental_id": rental["rental_id"],
            **filtered_result,
            "DateUpdated": time.strftime("%Y-%m-%d")
        }
        final_results.append(final_result)
    return final_results

def chunks(lst, n):
    for i in range(0, len(lst), n):
        yield lst[i:i + n]

logger = logging.getLogger(__name__)
scraper = AirbnbComSearchStrategy(logger)
needed_keys = ['host_name','listingId','url','orig_price_per_night', 'cleaning_fee', 'service_fee', 'total_price', 'price_per_night', 'check_in_date',
               'check_out_date']

final_results = []
errors = []

# Process the rental links in chunks of 3
for rental_chunk in chunks(rental_links, 3):
    with concurrent.futures.ThreadPoolExecutor() as executor:
        futures = [executor.submit(scrape_rental, rental, scraper, needed_keys) for rental in rental_chunk]

        for future in concurrent.futures.as_completed(futures):
            try:
                result = future.result()
                final_results.extend(result)
            except Exception as e:
                error_message = f"Error occurred: {e}"
                logger.error(error_message)
                errors.append(error_message)

end_time = time.time()

elapsed_time = end_time - start_time
minutes = int(elapsed_time // 60)
seconds = int(elapsed_time % 60)

# Define the scope and credentials for accessing Google Sheets
scope = ["https://spreadsheets.google.com/feeds", 'https://www.googleapis.com/auth/spreadsheets',
         "https://www.googleapis.com/auth/drive.file", "https://www.googleapis.com/auth/drive"]

# Load credentials from environment variable
creds_json = json.loads(os.getenv('GOOGLE_SHEETS_CREDENTIALS'))
creds = ServiceAccountCredentials.from_json_keyfile_dict(creds_json, scope)

# Authorize the client
client = gspread.authorize(creds)

# Open the Google Sheet by its name and select the specific sheet
spreadsheet_name = 'rankbreeze-sample-data-for-DB'
sheet_name = 'SearchResults'

spreadsheet = client.open(spreadsheet_name)
sheet = spreadsheet.worksheet(sheet_name)

# Convert the data to a Pandas DataFrame
df = pd.DataFrame(final_results)

# Append data to the sheet
existing_data = sheet.get_all_values()
existing_df = pd.DataFrame(existing_data[1:], columns=existing_data[0])

# Concatenate the existing data with the new data
new_df = pd.concat([existing_df, df], ignore_index=True)

# Write the updated DataFrame back to the sheet
set_with_dataframe(sheet, new_df)
