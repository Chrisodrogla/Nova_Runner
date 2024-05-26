
import sys
sys.path.insert(0,"C:\\Users\\calgo\\Downloads\\nova_scraper_\\scraper")

from scraper.strategies.airbnb_com.search_page import AirbnbComDetailStrategy
import logging

logger = logging.getLogger(__name__)

scraper = AirbnbComDetailStrategy(logger)
config = {"url": "https://www.airbnb.com/rooms/968187624157610437"}
result = scraper.execute(config)
print(result)




# needed_keys = ['guest', 'baths', 'beds', 'bedrooms']
#
# # Create a new dictionary with only the needed keys
# filtered_result = {key: result[key] for key in needed_keys}
#
# # Print the filtered result
# print(filtered_result)


# needed_keys = ['price_per_night','orig_price_per_night','cleaning_fee', 'service_fee', 'total_price']


# filtered_results = []


# for listing in result:
#     for item in listing:
#         filtered_result = {key: item[key] for key in needed_keys}
#         filtered_results.append(filtered_result)

# print(filtered_results)
# print(len(filtered_results))