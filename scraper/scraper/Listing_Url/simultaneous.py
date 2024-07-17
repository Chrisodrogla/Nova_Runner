import json
import sys
import time
import os
from urllib.parse import urlparse, parse_qs
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

def extract_dates_from_url(url):
    parsed_url = urlparse(url)
    query_params = parse_qs(parsed_url.query)
    check_in_date = query_params.get('checkin', [None])[0]
    check_out_date = query_params.get('checkout', [None])[0]
    return check_in_date, check_out_date

def scrape_rental(rental, scraper, needed_keys):
    config = {"url": rental["listing_link_format"]}
    result = scraper.execute(config)
    filtered_results = filter_results(result, needed_keys)
    final_results = []
    check_in_date, check_out_date = extract_dates_from_url(rental["listing_link_format"])
    for filtered_result in filtered_results:
        filtered_result['listingId'] = filtered_result['url'].split('/')[-1].split('?')[0]
        final_result = {
            "JobID": rental["JobID"],
            **filtered_result,
            "check_in_date": check_in_date,
            "check_out_date": check_out_date
        }
        final_results.append(final_result)
    return final_results

def chunks(lst, n):
    for i in range(0, len(lst), n):
        yield lst[i:i + n]

logger = logging.getLogger(__name__)
scraper = AirbnbComSearchStrategy(logger)
needed_keys = ['host_name', 'listingId', 'url', 'orig_price_per_night', 'cleaning_fee', 'service_fee', 'total_price', 'price_per_night']

final_results = []
errors = []

# Process each rental link individually
for rental in rental_links:
    try:
        rental_results = scrape_rental(rental, scraper, needed_keys)
        final_results.extend(rental_results)
    except Exception as e:
        error_message = f"Error occurred: {e} for JobID: {rental['JobID']}"
        logger.error(error_message)
        errors.append(error_message)

end_time = time.time()
elapsed_time = end_time - start_time
minutes = int(elapsed_time // 60)
seconds = int(elapsed_time % 60)

# Write the new data to the JSON file, replacing the existing data
with open('scraper/scraper/Listing_Url/output/final_results.json', 'w') as updated_file:
    json.dump(final_results, updated_file, indent=4)

print("Data replaced and saved to 'output/final_results.json'.")
print(final_results)
print("DONE SAMPLE")
print(f"Time taken: {minutes} minutes and {seconds} seconds")
