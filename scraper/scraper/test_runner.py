
import sys
sys.path.insert(0,"C:\\Users\\calgo\\Github_vscode_Cloned\\nova_scraper_-1\\scraper")

from scraper.strategies.airbnb_com.search_page import AirbnbComDetailStrategy
import logging

logger = logging.getLogger(__name__)

scraper = AirbnbComDetailStrategy(logger)
config = {"url": "https://www.airbnb.com/s/Davenport--Florida--United-States/homes?tab_id=home_tab&refinement_paths[]=/homes&flexible_trip_lengths[]=one_week&monthly_start_date=2024-06-01&monthly_length=3&monthly_end_date=2024-09-01&price_filter_input_type=0&channel=EXPLORE&source=structured_search_input_header&search_type=autocomplete_click&query=Davenport,%20Florida,%20United%20States&price_filter_num_nights=4&rank_mode=default&date_picker_type=calendar&checkin=2024-08-05&checkout=2024-08-09&min_bedrooms=5&min_beds=8&min_bathrooms=5&adults=13&currency=USD"}
result = scraper.execute(config)
# print(result)


#
# needed_keys = ['price_per_night','orig_price_per_night','cleaning_fee', 'service_fee', 'total_price']
#
# # Create a new dictionary with only the needed keys
# filtered_result = {key: result[key] for key in needed_keys}

# Print the filtered result
# print(result)



needed_keys = ['price_per_night','orig_price_per_night','cleaning_fee', 'service_fee', 'total_price']


filtered_results = []


for listing in result:
    for item in listing:
        filtered_result = {key: item[key] for key in needed_keys}
        filtered_results.append(filtered_result)

print(filtered_results)
print(len(filtered_results))