import time
import sys
sys.path.insert(0,"C:\\Users\\calgo\\PycharmProjects\\pythonProject\\nova_scraper_\\scraper")


from scraper.strategies.airbnb_com.search_page import    AirbnbComDetailStrategy #AirbnbComSearchStrategy
import logging

logger = logging.getLogger(__name__)

start_time = time.time()

scraper = AirbnbComDetailStrategy(logger)                  #AirbnbComDetailStrategy
config = {"url": "https://www.airbnb.ca/rooms/958036886603866738?adults=16&search_mode=regular_search&check_in=2024-09-02&check_out=2024-09-05&source_impression_id=p3_1722620518_P394zvvERqcaQaAi&previous_page_section_name=1000&federated_search_id=825a8c91-68d7-4a9b-a566-65c8c419a039"}


result = scraper.execute(config)

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

print(result)