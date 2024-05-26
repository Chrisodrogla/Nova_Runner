import json
import time
import os
import sys
sys.path.insert(0, os.path.join(os.getcwd(), "scraper"))

import concurrent.futures
from scraper.strategies.airbnb_com.search_page import AirbnbComSearchStrategy
import logging

sys.path.insert(0, os.path.join(os.getcwd(), "scraper"))

with open('scraper/scraper/Listing_Url/final_rental_link.json', 'r') as f:
    rental_links = json.load(f)

def filter_results(result, needed_keys):
    filtered_results = []
    for listing in result:
        for item in listing:
            filtered_result = {key: item.get(key, None) for key in needed_keys}
            filtered_results.append(filtered_result)
    return filtered_results

def scrape_rental(rental, scraper, needed_keys):
    config = {"url": rental["listing_link_format"]}
    backoff_time = 5  # Initial backoff time in seconds
    max_backoff_time = 60  # Maximum backoff time in seconds
    while True:
        try:
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
        except Exception as e:
            if "429" in str(e):
                print(f"Rate limit hit. Backing off for {backoff_time} seconds.")
                time.sleep(backoff_time)
                backoff_time = min(backoff_time * 2, max_backoff_time)  # Exponential backoff
            else:
                raise

logger = logging.getLogger(__name__)
scraper = AirbnbComSearchStrategy(logger)
needed_keys = ['orig_price_per_night', 'cleaning_fee', 'service_fee', 'total_price', 'price_per_night', 'check_in_date', 'check_out_date']

final_results = []
errors = []

with concurrent.futures.ThreadPoolExecutor() as executor:
    futures = [executor.submit(scrape_rental, rental, scraper, needed_keys) for rental in rental_links]

    for future in concurrent.futures.as_completed(futures):
        try:
            result = future.result()
            final_results.extend(result)
        except Exception as e:
            error_message = f"Error occurred: {e}"
            logger.error(error_message)
            errors.append(error_message)

print(final_results)
print("DONE SAMPLE")

# Print all errors at the end
if errors:
    print("\nErrors occurred during execution:")
    for error in errors:
        print(error)
