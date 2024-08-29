import json
import sys
import time
import os
from urllib.parse import urlparse, parse_qs
sys.path.insert(0, os.path.join(os.getcwd(), "scraper"))
import concurrent.futures
from scraper.strategies.airbnb_com.search_page import AirbnbComSearchStrategy
import logging
import jmespath

import pandas as pd

from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build
from datetime import datetime

batch_id = os.getenv('BATCH_ID', 'Batch1')
start_time = time.time()

with open('scraper/scraper/Listing_Url/json_file/final_rental_link.json', 'r') as f:
    data = json.load(f)
    rental_links = data[batch_id]

def filter_results(result, needed_keys):
    filtered_results = []
    for listing in result:
        for item in listing:
            filtered_result = {key: item.get(key, None) for key in needed_keys}
            # Split the url at '?' to keep only the base URL
            if 'url' in filtered_result:
                filtered_result['url'] = filtered_result['url'].split('?')[0]

            # Adding the new fields from to_add.py
            orig_price_per_night = jmespath.search("cohost.sections.sections[0].section.structuredDisplayPrice.explanationData.priceDetails[0].items[0].description", item) or \
                                   jmespath.search("cohost.sections.sections[1].section.structuredDisplayPrice.explanationData.priceDetails[0].items[0].description", item) or \
                                   jmespath.search("cohost.sections.sections[-1].section.structuredDisplayPrice.explanationData.priceDetails[0].items[0].description", item)

            total_price = jmespath.search("cohost.sections.sections[0].section.structuredDisplayPrice.explanationData.priceDetails[0].items[0].priceString", item) or \
                          jmespath.search("cohost.sections.sections[1].section.structuredDisplayPrice.explanationData.priceDetails[0].items[0].priceString", item) or \
                          jmespath.search("cohost.sections.sections[-1].section.structuredDisplayPrice.explanationData.priceDetails[0].items[0].priceString", item)

            total_without_tax = jmespath.search("cohost.sections.sections[0].section.structuredDisplayPrice.explanationData.priceDetails[1].items[0].priceString", item) or \
                                jmespath.search("cohost.sections.sections[1].section.structuredDisplayPrice.explanationData.priceDetails[1].items[0].priceString", item) or \
                                jmespath.search("cohost.sections.sections[-1].section.structuredDisplayPrice.explanationData.priceDetails[1].items[0].priceString", item)

            filtered_result['price_on_website'] = orig_price_per_night.split('x')[0].replace('$', '').strip().replace(',', '') if orig_price_per_night else None
            filtered_result['total_price_website'] = total_price.replace('$', '').strip().replace(',', '') if total_price else None
            filtered_result['total_on_website'] = total_without_tax.replace('$', '').strip().replace(',', '') if total_without_tax else None

            filtered_results.append(filtered_result)
    return filtered_results

def extract_dates_from_url(url):
    parsed_url = urlparse(url)
    query_params = parse_qs(parsed_url.query)
    check_in_date = query_params.get('checkin', [None])[0]
    check_out_date = query_params.get('checkout', [None])[0]
    return check_in_date, check_out_date

def scrape_rental(rental, needed_keys):
    logger = logging.getLogger(__name__)
    scraper = AirbnbComSearchStrategy(logger)
    config = {"url": rental["listing_link_format"]}
    result = scraper.execute(config)
    filtered_results = filter_results(result, needed_keys)
    final_results = []
    check_in_date, check_out_date = extract_dates_from_url(rental["listing_link_format"])
    for filtered_result in filtered_results:
        filtered_result['listingId'] = filtered_result['url'].split('/')[-1].split('?')[0]
        final_result = {
            "JobID": rental["JobID"],
            "InfoID": rental["InfoID"],
            **filtered_result,
            "check_in_date": check_in_date,
            "check_out_date": check_out_date
        }
        final_results.append(final_result)
    return final_results

def chunks(lst, n):
    for i in range(0, len(lst), n):
        yield lst[i:i + n]

logger = logging.getLogger(__name__)
needed_keys = ['rank','host_name', 'listingId', 'url', 'orig_price_per_night', 'cleaning_fee', 'service_fee', 'total_price', 'price_per_night','cohost']

final_results = []
errors = []

# Process the rental links in chunks of 3
for rental_chunk in chunks(rental_links, 3):
    with concurrent.futures.ThreadPoolExecutor() as executor:
        futures = {executor.submit(scrape_rental, rental, needed_keys): rental for rental in rental_chunk}

        for future in concurrent.futures.as_completed(futures):
            rental = futures[future]
            try:
                rental_results = future.result()
                final_results.extend(rental_results)
            except Exception as e:
                error_message = f"Error occurred: {e} for JobID: {rental['JobID']}"
                logger.error(error_message)
                errors.append(error_message)

end_time = time.time()
elapsed_time = end_time - start_time
minutes = int(elapsed_time // 60)
seconds = int(elapsed_time % 60)

# Google Sheets setup
SHEET_ID = '1S6gAIsjuYyGtOmWFGpF9okAPMWq6SnZ1zbIylBZqCt4'
MARKETDATA_SHEET_NAMES = ['JobTable_Results', 'JobTable_Results2', 'JobTable_Results3']

# Get Google Sheets credentials from environment variable
GOOGLE_SHEETS_CREDENTIALS = os.getenv("GOOGLE_SHEETS_CREDENTIALS")
credentials = Credentials.from_service_account_info(json.loads(GOOGLE_SHEETS_CREDENTIALS))

# Create Google Sheets API service
service = build("sheets", "v4", credentials=credentials)

# Add Run_Date column to the final_results
for result in final_results:
    result['Run_Date'] = datetime.now().strftime('%Y-%m-%d')

df = pd.DataFrame(final_results)

def get_sheet_cell_count(sheet_name):
    sheet = service.spreadsheets().get(spreadsheetId=SHEET_ID, ranges=[sheet_name], includeGridData=False).execute()
    sheet_info = sheet['sheets'][0]
    return sheet_info['properties']['gridProperties']['rowCount'] * sheet_info['properties']['gridProperties']['columnCount']

def append_to_sheet(sheet_name, data):
    service.spreadsheets().values().append(
        spreadsheetId=SHEET_ID,
        range=f"{sheet_name}!A2",
        valueInputOption="RAW",
        body={"values": data}
    ).execute()

# Check each sheet for available space and append data accordingly
for sheet_name in MARKETDATA_SHEET_NAMES:
    try:
        cell_count = get_sheet_cell_count(sheet_name)
        if cell_count + df.size <= 10000000:
            append_to_sheet(sheet_name, df.values.tolist())
            break
    except Exception as e:
        error_message = f"Error occurred: {e} while appending data to {sheet_name}"
        logger.error(error_message)
        errors.append(error_message)
