import time
import sys
sys.path.insert(0,"C:\\Users\\calgo\\PycharmProjects\\pythonProject\\nova_scraper_\\scraper")


from scraper.strategies.airbnb_com.search_page import    AirbnbComDetailStrategy #AirbnbComSearchStrategy
import logging

logger = logging.getLogger(__name__)

start_time = time.time()

scraper = AirbnbComDetailStrategy(logger)                  #AirbnbComDetailStrategy
config = {"url": "https://www.airbnb.com/rooms/834175163702868485?source_impression_id=p3_1722365712_P3r9GGsYnpZvPh-d&check_in=2024-08-05&guests=1&adults=1&check_out=2024-08-08"}



result = scraper.execute(config)


############################################################################################################################################################

# needed_keys = ['guest', 'baths', 'beds', 'bedrooms']
# needed_keys = ['host_name', 'cleaning_fee', 'service_fee', 'price_per_night']
# needed_keys = ['cohost']
# needed_keys = ['cleaning_fee', 'service_fee']
# Create a new dictionary with only the needed keys
# filtered_result = {key: result[key] for key in needed_keys}

# Print the filtered result

# print("##################################################################################################################################################################################")

# print(result)
# print(filtered_result)



# ############################################################################################################################################################
# needed_keys = ['price','cleaning_fee', 'service_fee', 'total_price', 'price_per_night','total_price']
# # needed_keys = ['service_fee']
#
# filtered_results = []
#
#
# for listing in result:
#     for item in listing:
#         filtered_result = {key: item[key] for key in needed_keys}
#         filtered_results.append(filtered_result)
#
# print(filtered_results)
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

#############################################################################################################################################################
print(result)