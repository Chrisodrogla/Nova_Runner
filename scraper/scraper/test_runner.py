import time
import sys
sys.path.insert(0,"C:\\Users\\calgo\\PycharmProjects\\pythonProject\\nova_scraper_\\scraper")


from scraper.strategies.airbnb_com.search_page import AirbnbComSearchStrategy #AirbnbComDetailStrategy
import logging

logger = logging.getLogger(__name__)

start_time = time.time()

scraper = AirbnbComSearchStrategy(logger)                  #AirbnbComDetailStrategy
config = {"url": "https://www.airbnb.ca/s/Davenport--Florida--United-States/homes?date_picker_type=calendar&checkin=2024-09-09&checkout=2024-09-12&adults=28&search_mode=regular_search&min_bedrooms=10&tab_id=home_tab&refinement_paths%5B%5D=%2Fhomes&query=Davenport%2C%20Florida%2C%20United%20States&place_id=ChIJ7WLP2TJx3YgRrFN8JGEANew&flexible_trip_lengths%5B%5D=one_week&monthly_start_date=2024-08-01&monthly_length=3&monthly_end_date=2024-11-01&price_filter_input_type=0&price_filter_num_nights=3&channel=EXPLORE&ne_lat=28.405743790161548&ne_lng=-81.46626269012353&sw_lat=28.399925950373&sw_lng=-81.47221834028511&zoom=16.735491783306536&zoom_level=16.735491783306536&search_by_map=true&search_type=user_map_move"}



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



# ############################################################################################################################################################
needed_keys = ['price','cleaning_fee', 'service_fee', 'total_price', 'price_per_night','total_price']
# needed_keys = ['service_fee']

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

#############################################################################################################################################################
# print(result)