import time
import sys

sys.path.insert(0, "C:\\Users\\calgo\\PycharmProjects\\pythonProject\\nova_scraper_\\scraper")

from scraper.strategies.airbnb_com.search_page import AirbnbComSearchStrategy
import logging

logger = logging.getLogger(__name__)

start_time = time.time()

scraper = AirbnbComSearchStrategy(logger)
config = {
    "url": "https://www.airbnb.ca/s/Davenport--Florida--United-States/homes?date_picker_type=calendar&checkin=2024-09-02&checkout=2024-09-05&adults=16&min_bedrooms=8&tab_id=home_tab&refinement_paths%5B%5D=%2Fhomes&query=Davenport%2C%20Florida%2C%20United%20States&place_id=ChIJ7WLP2TJx3YgRrFN8JGEANew&flexible_trip_lengths%5B%5D=one_week&monthly_start_date=2024-09-01&monthly_length=3&monthly_end_date=2024-12-01&search_mode=regular_search&price_filter_input_type=0&price_filter_num_nights=3&channel=EXPLORE&ne_lat=28.319260880857072&ne_lng=-81.45874706072539&sw_lat=28.31797568050151&sw_lng=-81.46041060063646&zoom=19.819766636170648&zoom_level=19.819766636170648&search_by_map=true&search_type=user_map_move"
}

result = scraper.execute(config)

# needed_keys = ['rank','host_name', 'listingId', 'url', 'orig_price_per_night', 'cleaning_fee', 'service_fee', 'total_price', 'price_per_night']

needed_keys = ['rank', 'host_name', 'orig_price_per_night', 'discounted_price', 'Cleaning fee', 'Airbnb service fee',
               'total_price', 'price_per_night']


def extract_value(data, path):
    for key in path:
        if isinstance(data, list):
            data = data[0] if data else {}
        data = data.get(key, {})
    return data


filtered_results = []

for listing in result:
    for item in listing:
        original_price = extract_value(item, ['cohost', 'sections', 'sections', 'section', 'structuredDisplayPrice',
                                           'explanationData', 'priceDetails', 'items', 'explanationData','priceDetails','items','priceString'])
        discounted_price = extract_value(item, ['cohost', 'sections', 'sections', 'section', 'structuredDisplayPrice',
                                                'primaryLine', 'discountedPrice'])
        items_path = ['cohost', 'sections', 'sections', 'section', 'structuredDisplayPrice',
                      'explanationData', 'priceDetails', 'items']
        items = extract_value(item, items_path)
        cleaning_fee = items[1]['priceString'] if isinstance(items, list) and len(items) > 1 else None

        service_fee = items[2]['priceString'] if isinstance(items, list) and len(items) > 1 else None
        Total_total = extract_value(item, ['cohost', 'sections', 'sections', 'section', 'structuredDisplayPrice',
                                            'explanationData', 'priceDetails', 'items', 'priceString'])

        filtered_result = {
            'rank': item['rank'],
            'host_name': item['host_name'],
            'orig_price_per_night': original_price,
            'discounted_price': discounted_price,
            'Cleaning fee': cleaning_fee,
            'Airbnb service fee': service_fee,
            'total_price': Total_total,
            'price_per_night': original_price
        }
        filtered_results.append(filtered_result)

print(filtered_results)


