import json
import sys
import logging
import time
import os

start_time = time.time()

# Add the 'scraper' directory to the sys.path
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
    # Print the current working directory
    print("Current working directory:", os.getcwd())

    # File paths
    base_path = os.path.dirname(__file__)
    input_file = os.path.join(base_path, 'json_file/json_file/rb_bnb.json')
    output_file = os.path.join(base_path, 'json_file/json_file/listing_attribute.json')
    target_file = os.path.join(base_path, 'json_file/json_file/target_list.json')

    # Read the target list
    target_list = read_json_file(target_file)

    # Extract target IDs
    target_ids = {item['link'].split('/')[-1] for item in target_list}

    # Read the input data
    data = read_json_file(input_file)

    # Filter the data
    filtered_data = [item for item in data if item['airbnb_link'].split('/')[-1] in target_ids]

    # Initialize the scraper
    scraper = AirbnbComDetailStrategy(logger)

    # Scrape the Airbnb details
    updated_data = scrape_airbnb_details(filtered_data, scraper)

    # Write the updated data to the output file
    write_json_file(updated_data, output_file)

    print(f"Data has been successfully written to {output_file}")

if __name__ == "__main__":
    main()

end_time = time.time()

elapsed_time = end_time - start_time
minutes = int(elapsed_time // 60)
seconds = int(elapsed_time % 60)
print(f"Time takes {minutes} minutes and {seconds} seconds")
