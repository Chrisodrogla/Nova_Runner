import time
import sys
import logging

sys.path.insert(0, "C:\\Users\\calgo\\PycharmProjects\\pythonProject\\nova_scraper_\\scraper")
from scraper.strategies.airbnb_com.search_page import AirbnbComDetailStrategy  # AirbnbComDetailStrategy

logger = logging.getLogger(__name__)

start_time = time.time()

scraper = AirbnbComDetailStrategy(logger)  # AirbnbComDetailStrategy
config = {
    "url": "https://www.airbnb.ca/rooms/1047224676448180120?adults=16&search_mode=regular_search&check_in=2024-09-16&source_impression_id=p3_1722866587_P3LpbdB_iQhjA6OR&previous_page_section_name=1000&federated_search_id=6b639a26-703b-4e79-822e-f5001e93cb89&guests=1&check_out=2024-09-20"
}

result = scraper.execute(config)

needed_keys = ['orig_price_per_night', 'discounted_price', 'Cleaning fee', 'Airbnb service fee', 'total_price', 'price_per_night']

def extract_value(data, path):
    for key in path:
        if isinstance(data, list):
            data = data[0] if data else {}
        if not isinstance(data, dict):
            return None  # Early return if data is not a dictionary
        data = data.get(key, {})
    return data if isinstance(data, (dict, list)) else None  # Ensure to return None if final data is not dict or list

filtered_results = []

primary_line_path = ['cohost', 'sections', 'sections', 'section', 'structuredDisplayPrice', 'primaryLine', 'price']
original_price = extract_value(result, primary_line_path)

items_path = ['cohost', 'sections', 'sections', 'section', 'structuredDisplayPrice', 'explanationData', 'priceDetails']
price_details = extract_value(result, items_path)

if isinstance(price_details, list) and len(price_details) > 0:
    items = price_details[0].get('items', [])
    original_price = items[0].get('description') if len(items) > 0 else None
    total_price = items[0].get('priceString') if len(items) > 0 else None

else:
    total_price = cleaning_fee = service_fee = None

filtered_result = {
    'host_name': result.get('host_name'),
    'orig_price_per_night': original_price.split('x')[0] if 'x' in original_price else original_price,
    'Cleaning fee': result.get('cleaning_fee'),
    'Airbnb service fee': result.get('service_fee'),
    'total_price': total_price,
    'price_per_night': original_price.split('x')[0] if 'x' in original_price else original_price
}

filtered_results.append(filtered_result)

print(filtered_results)
# print(result)