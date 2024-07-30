import json
import csv
import sys
import time
import os
# sys.path.insert(0, "C:\\Users\\calgo\\PycharmProjects\\pythonProject\\nova_scraper_\\scraper")
sys.path.insert(0, os.path.join(os.getcwd(), "scraper"))
import concurrent.futures
from scraper.strategies.airbnb_com.search_page import AirbnbComSearchStrategy
import logging

import pandas as pd

from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build
from datetime import datetime

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
        filtered_result['listingId'] = filtered_result['url'].split('/')[-1].split('?')[0]
        final_result = {
            "rental_id": rental["rental_id"],
            **filtered_result
        }
        final_results.append(final_result)
    return final_results

def chunks(lst, n):
    for i in range(0, len(lst), n):
        yield lst[i:i + n]

logger = logging.getLogger(__name__)
scraper = AirbnbComSearchStrategy(logger)
needed_keys = ['host_name', 'listingId', 'url', 'orig_price_per_night', 'cleaning_fee', 'service_fee', 'total_price', 'price_per_night', 'check_in_date', 'check_out_date']

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

# # Write the new data to the JSON file, replacing the existing data
# with open('scraper/scraper/Listing_Url/output/final_results.json', 'w') as updated_file:
#     json.dump(final_results, updated_file, indent=4)

print("Data replaced and saved to 'output/final_results.json'.")
print(final_results)
print("DONE SAMPLE")
print(f"Time takes {minutes} minutes and {seconds} seconds")

# Google Sheets setup
SHEET_ID = '10OgYeu7oj5Lwtr4gGy14zXuZlAk0gibSbgq_AmUtf7Q'
MARKETDATA_SHEET_NAME = 'JobTable_Results'


# Get Google Sheets credentials from environment variable
GOOGLE_SHEETS_CREDENTIALS = os.getenv("GOOGLE_SHEETS_CREDENTIALS")
credentials = Credentials.from_service_account_info(json.loads(GOOGLE_SHEETS_CREDENTIALS))

# Create Google Sheets API service
service = build("sheets", "v4", credentials=credentials)


df = pd.DataFrame(final_results)

# # Clear all data below header in the "Review" sheet
# service.spreadsheets().values().clear(
#     spreadsheetId=SHEET_ID,
#     range=f"{MARKETDATA_SHEET_NAME}!A2:Z"
# ).execute()

# Write new data to the "Review" sheet starting from row 2
service.spreadsheets().values().update(
    spreadsheetId=SHEET_ID,
    range=f"{MARKETDATA_SHEET_NAME}!A2",
    valueInputOption="RAW",
    body={"values": df.values.tolist()}
).execute()
