import time
import sys
import logging
import json
import jmespath

sys.path.insert(0, "C:\\Users\\calgo\\PycharmProjects\\pythonProject\\nova_scraper_\\scraper")
from scraper.strategies.airbnb_com.search_page import AirbnbComDetailStrategy  # AirbnbComDetailStrategy

logger = logging.getLogger(__name__)

start_time = time.time()

scraper = AirbnbComDetailStrategy(logger)  # AirbnbComDetailStrategy
config = {
    "url": "https://www.airbnb.ca/rooms/50418580?adults=10&children=2&enable_m3_private_room=true&infants=0&pets=0&search_mode=regular_search&check_in=2024-09-14&check_out=2024-09-18&source_impression_id=p3_1724755680_P3qjeP-ucE9Vm7EM&previous_page_section_name=1000&federated_search_id=bf8dce51-ff32-41d1-b074-fdf6deb9ca91"
}

result = scraper.execute(config)

# Define the JMESPath expressions
orig_price_per_night_path = "cohost.sections.sections[0].section.structuredDisplayPrice.explanationData.priceDetails[0].items[0].description"
orig_price_per_night_path1 = "cohost.sections.sections[1].section.structuredDisplayPrice.explanationData.priceDetails[0].items[0].description"

total_price_path = "cohost.sections.sections[0].section.structuredDisplayPrice.explanationData.priceDetails[0].items[0].priceString"
total_price_path1 = "cohost.sections.sections[1].section.structuredDisplayPrice.explanationData.priceDetails[0].items[0].priceString"


# Use jmespath to extract the values
orig_price_per_night = jmespath.search(orig_price_per_night_path, result) or jmespath.search(orig_price_per_night_path1, result)
total_price = jmespath.search(total_price_path, result) or jmespath.search(total_price_path1, result)

orig_price_per_night_vale = orig_price_per_night.split('x')[0].replace('$', '').strip(' ')

# Prepare the filtered result
filtered_result = {
    'host_name': result.get('host_name'),
    'orig_price_per_night':orig_price_per_night_vale ,
    'Cleaning fee': result.get('cleaning_fee'),
    'Airbnb service fee': result.get('service_fee'),
    'total_price': total_price.strip('$'),
    'price_per_night': orig_price_per_night_vale
}

# Save the result to a JSON file
with open('listing_price.json', 'w') as json_file:
    json.dump(filtered_result, json_file, indent=4)
with open('listing_price2.json', 'w') as json_file:
    json.dump(result, json_file, indent=4)


print(orig_price_per_night)
