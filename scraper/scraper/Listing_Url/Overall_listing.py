
import json
import csv
import sys
sys.path.insert(0,"C:\\Users\\calgo\\Downloads\\nova_scraper_\\scraper")


from scraper.strategies.airbnb_com.search_page import AirbnbComSearchStrategy
import logging


with open('final_rental_link.json', 'r') as f:
    rental_links = json.load(f)


def filter_results(result, needed_keys):
    filtered_results = []
    for listing in result:
        for item in listing:
            filtered_result = {key: item.get(key, None) for key in needed_keys}
            filtered_results.append(filtered_result)
    return filtered_results


logger = logging.getLogger(__name__)
scraper = AirbnbComSearchStrategy(logger)
needed_keys = ['orig_price_per_night', 'cleaning_fee', 'service_fee', 'total_price', 'price_per_night', 'check_in_date',
               'check_out_date']

final_results = []


for rental in rental_links:
    config = {"url": rental["listing_link_format"]}
    result = scraper.execute(config)
    filtered_results = filter_results(result, needed_keys)

    for filtered_result in filtered_results:
        final_result = {
            "rankbreeze_Id": rental["rankbreeze_Id"],
            "rental_id": rental["rental_id"],
            **filtered_result
        }
        final_results.append(final_result)


with open('final_results.json', 'w') as f:
    json.dump(final_results, f, indent=4)

csv_columns = ['rankbreeze_Id', 'rental_id'] + needed_keys

with open('final_results.csv', 'w', newline='') as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames=csv_columns)
    writer.writeheader()
    for data in final_results:
        writer.writerow(data)
