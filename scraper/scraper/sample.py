import time
import sys
import json
import logging

# Insert the path to your scraper module
sys.path.insert(0, "C:\\Users\\calgo\\PycharmProjects\\pythonProject\\nova_scraper_\\scraper")

from scraper.strategies.airbnb_com.search_page import AirbnbComSearchStrategy  # AirbnbComDetailStrategy

# Configure logging
logging.basicConfig(
    filename='scraper.log',  # Name of the log file
    level=logging.DEBUG,     # Set the logging level
    format='%(asctime)s - %(levelname)s - %(message)s'  # Log format
)

logger = logging.getLogger(__name__)

# Log the start time
start_time = time.time()
logger.info('Script started')

# Initialize the scraper
scraper = AirbnbComSearchStrategy(logger)
logger.info('Initialized AirbnbComSearchStrategy scraper')

# Configuration for the scraper
config = {
    "url": "https://www.airbnb.ca/s/Kissimmee--Florida--United-States/homes?tab_id=home_tab&refinement_paths%5B%5D=%2Fhomes&flexible_trip_lengths%5B%5D=one_week&monthly_start_date=2024-09-01&monthly_length=3&monthly_end_date=2024-12-01&price_filter_input_type=2&channel=EXPLORE&date_picker_type=calendar&checkin=2024-09-15&checkout=2024-09-20&adults=10&children=2&query=Kissimmee%2C%20FL&place_id=ChIJ5wsVNxqE3YgRDcL9EZfN55Q&source=structured_search_input_header&search_type=user_map_move&search_mode=regular_search&price_filter_num_nights=5&ne_lat=28.321700775108848&ne_lng=-81.59466641430089&sw_lat=28.320156375263316&sw_lng=-81.59623643103083&zoom=19.48151869296618&zoom_level=19.48151869296618&search_by_map=true"
}

logger.info('Configuration set for the scraper')

# Execute the scraper
try:
    logger.info('Starting scraper execution')
    result = scraper.execute(config)
    logger.info('Scraper execution completed')
except Exception as e:
    logger.error(f'Error during scraper execution: {e}')

# Log the result
logger.debug(f'Scraper result: {json.dumps(result, indent=2)}')

# Log the end time
end_time = time.time()
elapsed_time = end_time - start_time
logger.info(f'Script finished, elapsed time: {elapsed_time:.2f} seconds')

# Print the result to the console
print(result)
