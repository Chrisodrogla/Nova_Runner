import time
import sys
sys.path.insert(0,"C:\\Users\\calgo\\PycharmProjects\\pythonProject\\nova_scraper_\\scraper")


from scraper.strategies.airbnb_com.search_page import AirbnbComSearchStrategy #AirbnbComDetailStrategy
import logging

logger = logging.getLogger(__name__)

start_time = time.time()

scraper = AirbnbComSearchStrategy(logger)                  #AirbnbComDetailStrategy
config = {"url": "https://www.airbnb.ca/s/Davenport--Florida--United-States/homes?date_picker_type=calendar&currency=USD&checkin=2024-09-09&checkout=2024-09-12&adults=28&search_mode=regular_search&min_bedrooms=10&  "}



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
needed_keys = ['orig_price_per_night','cleaning_fee', 'service_fee', 'total_price', 'price_per_night','total_price']


filtered_results = []


for listing in result:
    for item in listing:
        filtered_result = {key: item[key] for key in needed_keys}
        filtered_results.append(filtered_result)

print(filtered_results)
print(len(filtered_results))

# Record the end time
end_time = time.time()

# Calculate the elapsed time
elapsed_time = end_time - start_time
minutes = int(elapsed_time // 60)
seconds = int(elapsed_time % 60)

print(f"Time takes {minutes} minutes and {seconds} seconds")

#
# print(result)