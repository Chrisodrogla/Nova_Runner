import time
import sys
sys.path.insert(0,"C:\\Users\\calgo\\PycharmProjects\\pythonProject\\nova_scraper_\\scraper")
import json

from scraper.strategies.airbnb_com.search_page import AirbnbComSearchStrategy #AirbnbComDetailStrategy
import logging

logger = logging.getLogger(__name__)

start_time = time.time()

scraper =AirbnbComSearchStrategy(logger)                  #AirbnbComSearchStrategy
config = {"url": "https://www.airbnb.ca/s/Kissimmee--Florida--United-States/homes?tab_id=home_tab&refinement_paths%5B%5D=%2Fhomes&flexible_trip_lengths%5B%5D=one_week&monthly_start_date=2024-09-01&monthly_length=3&monthly_end_date=2024-12-01&price_filter_input_type=2&channel=EXPLORE&date_picker_type=calendar&checkin=2024-09-15&checkout=2024-09-20&adults=10&children=2&query=Kissimmee%2C%20FL&place_id=ChIJ5wsVNxqE3YgRDcL9EZfN55Q&source=structured_search_input_header&search_type=user_map_move&search_mode=regular_search&price_filter_num_nights=5&ne_lat=28.321700775108848&ne_lng=-81.59466641430089&sw_lat=28.320156375263316&sw_lng=-81.59623643103083&zoom=19.48151869296618&zoom_level=19.48151869296618&search_by_map=true"}



result = scraper.execute(config)


############################################################################################################################################################

# needed_keys = ['guest', 'baths', 'beds', 'bedrooms']
# needed_keys = ['cohost']

# Create a new dictionary with only the needed keys
# filtered_result = {key: result[key] for key in needed_keys}

# Print the filtered result

# print("##################################################################################################################################################################################")

# print(result)
# print(filtered_result)



############################################################################################################################################################
# needed_keys = ['rank','host_name', 'url', 'orig_price_per_night', 'cleaning_fee', 'service_fee', 'total_price', 'price_per_night']
#
# filtered_results = []
#
#
# for listing in result:
#     for item in listing:
#         filtered_result = {key: item[key] for key in needed_keys}
#         filtered_results.append(filtered_result)
#
# # print(filtered_results)
# # print(len(filtered_results))
#
# # Record the end time
# end_time = time.time()
#
# # Calculate the elapsed time
# elapsed_time = end_time - start_time
# minutes = int(elapsed_time // 60)
# seconds = int(elapsed_time % 60)
#
# print(f"Time takes {minutes} minutes and {seconds} seconds")
#
# #
# print(result)

# Write filtered results to JSON file
with open('4_results.json', 'w') as outfile:
    json.dump(result, outfile, indent=4)  # indent for readability

