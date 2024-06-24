import json
import sys
import logging
import time
import os


# Add the 'scraper' directory to the sys.path
sys.path.insert(0, os.path.join(os.getcwd(), "scraper"))

start_time = time.time()

sys.path.insert(0, 'scraper/scraper')

from scraper.strategies.airbnb_com.search_page import AirbnbComDetailStrategy

logger = logging.getLogger(__name__)

def read_json_file(file_path):
    with open(file_path, 'r') as file:
        return json.load(file)

def write_json_file(data, file_path):
    with open(file_path, 'w') as file:
        json.dump(data, file, indent=4)

def scrape_airbnb_details(data, scraper):
    updated_data = []
    needed_keys = ['guest', 'baths', 'beds', 'bedrooms']

    for item in data:
        config = {"url": item['airbnb_link']}
        result = scraper.execute(config)

        # Create a new dictionary with only the needed keys
        filtered_result = {key: result[key] for key in needed_keys}

        # Combine the original item with the filtered result
        combined_result = {**item, **filtered_result}
        updated_data.append(combined_result)

    return updated_data

def main():
    # File paths
    input_file = 'scraper/scraper/Listing_Url/json_file/rb_bnb.json'
    output_file = 'scraper/scraper/Listing_Url/json_file/listing_attribute.json'
    target_file = 'scraper/scraper/Listing_Url/json_file/target_list.json'

    data = read_json_file(input_file)
    target_list = read_json_file(target_file)

    target_ids = {item['link'].split('/')[-1] for item in target_list}

    # Create a dictionary to ensure only one entry per target ID
    filtered_data_dict = {}

    for item in data:
        item_id = item['airbnb_link'].split('/')[-1]
        if item_id in target_ids and item_id not in filtered_data_dict:
            filtered_data_dict[item_id] = item

    filtered_data = list(filtered_data_dict.values())

    scraper = AirbnbComDetailStrategy(logger)

    updated_data = scrape_airbnb_details(filtered_data, scraper)

    write_json_file(updated_data, output_file)

    print(f"Data has been successfully written to {output_file}")

if __name__ == "__main__":
    main()

end_time = time.time()

elapsed_time = end_time - start_time
minutes = int(elapsed_time // 60)
seconds = int(elapsed_time % 60)
print(f"Time takes {minutes} minutes and {seconds} seconds")
