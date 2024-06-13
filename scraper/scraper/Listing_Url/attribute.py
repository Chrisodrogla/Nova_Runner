import json
import sys
import logging
import time
import os

start_time = time.time()

# sys.path.insert(0, "C:\\Users\\calgo\\PycharmProjects\\pythonProject\\nova_scraper_\\scraper")
sys.path.insert(0, os.path.join(os.getcwd(), "scraper"))
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
    # with open('json_file/final_rental_link.json', 'r') as f:
    input_file = 'scraper/scraper/Listing_Url/json_file/json_file/rb_bnb.json'
    output_file = 'scraper/scraper/Listing_Url/json_file/son_file/listing_attribute.json'
    target_file = 'scraper/scraper/Listing_Url/json_file/json_file/target_list.json'
    target_list = read_json_file(target_file)

    target_ids = {item['link'].split('/')[-1] for item in target_list}

    filtered_data = [item for item in data if item['airbnb_link'].split('/')[-1] in target_ids]

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
