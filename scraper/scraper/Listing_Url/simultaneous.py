import json
import csv
import sys
import os
sys.path.insert(0, os.path.join(os.getcwd(), "scraper"))
import concurrent.futures
from scraper.strategies.airbnb_com.search_page import AirbnbComSearchStrategy
import logging

with open('scraper/scraper/Listing_Url/final_rental_link.json', 'r') as f:
    rental_links = json.load(f)

# # sys.path.insert(0, "C:\\Users\\calgo\Github_vscode_Cloned\\nova_scraper_-1\\scraper") #scraper
# import concurrent.futures
# from scraper.strategies.airbnb_com.search_page import AirbnbComSearchStrategy
# import logging




# with open('C:\\Users\\calgo\\Github_vscode_Cloned\\nova_scraper_-1\\scraper\\scraper\\Listing_Url\\final_rental_link.json', 'r') as f:
#     rental_links = json.load(f)


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


logger = logging.getLogger(__name__)
scraper = AirbnbComSearchStrategy(logger)
needed_keys = ['orig_price_per_night', 'cleaning_fee', 'service_fee', 'total_price', 'price_per_night', 'check_in_date',
               'check_out_date']


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


# with open('final_results.json', 'w') as f:
#     json.dump(final_results, f, indent=4)


# csv_columns = ['rankbreeze_Id', 'rental_id'] + needed_keys
# with open('final_results.csv', 'w', newline='') as csvfile:
#     writer = csv.DictWriter(csvfile, fieldnames=csv_columns)
#     writer.writeheader()
#     for data in final_results:
#         writer.writerow(data)


print(final_results)
print("DONE SAMPLE")

# Print all errors at the end
if errors:
    print("\nErrors occurred during execution:")
    for error in errors:
        print(error)
