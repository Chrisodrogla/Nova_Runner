
import sys
sys.path.insert(0,"C:\\Users\\calgo\\Github_vscode_Cloned\\nova_scraper_-1\\scraper")

from scraper.strategies.airbnb_com.search_page import AirbnbComDetailStrategy
import logging

logger = logging.getLogger(__name__)

scraper = AirbnbComDetailStrategy(logger)
config = {"url": "https://www.airbnb.com/rooms/713932389993706415?category_tag=Tag%3A8851&enable_m3_private_room=true&search_mode=flex_destinations_search&check_in=2024-07-28&check_out=2024-07-31&source_impression_id=p3_1722017227_P3B910jZU9nSTxtJ&previous_page_section_name=1000&federated_search_id=7536b9e1-13d9-4c2e-b142-7f29fa8030ec"}
result = scraper.execute(config)

print(result)
