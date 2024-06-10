import json
import csv
import sys
import time
import os
import gspread
from oauth2client.service_account import ServiceAccountCredentials


# sys.path.insert(0, "C:\\Users\\calgo\\PycharmProjects\\pythonProject\\nova_scraper_\\scraper")
sys.path.insert(0, os.path.join(os.getcwd(), "scraper"))
import concurrent.futures
from scraper.strategies.airbnb_com.search_page import AirbnbComSearchStrategy
import logging
batch_id = os.getenv('BATCH_ID', 'Batch1')
start_time = time.time()

# # with open('scraper/scraper/Listing_Url/final_rental_link.json', 'r') as f:
# with open('json_file/final_rental_link.json', 'r') as f:
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
            "rankbreeze_Id": rental["rankbreeze_Id"],
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
needed_keys = ['orig_price_per_night', 'cleaning_fee', 'service_fee', 'total_price', 'price_per_night', 'check_in_date',
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

# Load existing data from the JSON file
existing_data = []

# with open('output/final_results.json', 'r') as existing_file:
with open('scraper/scraper/Listing_Url/output/final_results.json', 'r') as existing_file:
    existing_data = json.load(existing_file)

# Append your new data to the existing list
existing_data.extend(final_results)

# Write the updated data back to the JSON file
# with open('output/final_results.json', 'w') as updated_file:
with open('scraper/scraper/Listing_Url/output/final_results.json', 'w') as updated_file:
    json.dump(existing_data, updated_file, indent=4)

print("Data appended and saved to 'output/final_results.json'.")

print(final_results)
print("DONE SAMPLE")



print(f"Time takes {minutes} minutes and {seconds} seconds")





scope = ["https://spreadsheets.google.com/feeds", 'https://www.googleapis.com/auth/spreadsheets',
         "https://www.googleapis.com/auth/drive.file", "https://www.googleapis.com/auth/drive"]

# Load credentials from environment variable
creds_json = json.loads(os.getenv('GOOGLE_SHEETS_CREDENTIALS'))
creds = ServiceAccountCredentials.from_json_keyfile_dict(creds_json, scope)

# Authorize the client
client = gspread.authorize(creds)

# Open the Google Sheet by its name
sheet = client.open("SearchResults").sheet1

# Prepare data in the format needed for appending
rows = [[
    item['rankbreeze_Id'],
    item['rental_id'],
    item['orig_price_per_night'],
    item['cleaning_fee'],
    item['service_fee'],
    item['total_price'],
    item['price_per_night'],
    item['check_in_date'],
    item['check_out_date']
] for item in final_results]

# Append data to the sheet
for row in rows:
    sheet.append_row(row)