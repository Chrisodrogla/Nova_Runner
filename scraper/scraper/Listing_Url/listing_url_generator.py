import json
from datetime import datetime, timedelta
import sys
sys.path.insert(0, 'scraper/scraper')

def generate_listing_link(address, start_date, end_date, delta_days, guest, bedrooms, beds, bath):
    base_url = f"https://www.airbnb.com/s/{address}/homes"
    params = {
        "tab_id": "home_tab",
        "refinement_paths[]": "/homes",
        "flexible_trip_lengths[]": "one_week",
        "monthly_start_date": "2024-06-01",
        "monthly_length": "3",
        "monthly_end_date": "2024-09-01",
        "price_filter_input_type": "0",
        "channel": "EXPLORE",
        "source": "structured_search_input_header",
        "search_type": "autocomplete_click",
        "query": f"{address.split('--')[0]},%20{address.split('--')[1]},%20United%20States",
        "price_filter_num_nights": delta_days,
        "rank_mode": "default",
        "date_picker_type": "calendar",
        "checkin": start_date,
        "checkout": end_date,
        "min_bedrooms": bedrooms,
        "min_beds": beds,
        "min_bathrooms": bath,
        "adults": guest,
        "currency": "USD"
    }

    params_string = '&'.join([f"{key}={value}" for key, value in params.items()])
    listing_link = f"{base_url}?{params_string}"

    return listing_link

def get_next_weekday(start_date, target_weekday, weeks_in_advance=3):
    days_ahead = target_weekday - start_date.weekday()
    if days_ahead < 0:
        days_ahead += 7
    next_weekday = start_date + timedelta(days_ahead + 7 * weeks_in_advance)
    return next_weekday

# Parameters
number_of_weeks = 1  # Number of weeks for each listing
days_in_week = 4  # Wednesday to Saturday
weeks_in_advance = 6  # Start date is 6 weeks from today (can be adjusted)
target_weekday = 0  # Monday0 Tuesday1 .....

# Current date
current_date = datetime.now().date()
start_date = get_next_weekday(current_date, target_weekday, weeks_in_advance)

# JSON data from file
with open('scraper/scraper/Listing_Url/json_file/listing_attribute.json', 'r') as f:
    listings = json.load(f)

output = []

for listing in listings:
    address = listing["address"]
    guest = listing["guest"]
    baths = listing["baths"]
    beds = listing["beds"]
    bedrooms = listing["bedrooms"]
    airbnb_link = listing["airbnb_link"]

    for i in range(number_of_weeks):
        current_start_date = start_date + timedelta(weeks=i)
        current_end_date = current_start_date + timedelta(days=days_in_week)
        delta_days = (current_end_date - current_start_date).days

        listing_link = generate_listing_link(address, current_start_date.isoformat(), current_end_date.isoformat(), delta_days, guest, bedrooms, beds, baths)
        rental_id = airbnb_link.replace("https://www.airbnb.com/rooms/", "")

        output_entry = {
            "listing_link_format": listing_link,
            'airbnb_link': airbnb_link,
            "rental_id": rental_id,
            "beds": beds,
            "guest": guest,
            "bedrooms": bedrooms,
            "baths": baths,
            "start_date": current_start_date.isoformat(),
            "end_date": current_end_date.isoformat()
        }

        output.append(output_entry)

# Split the output into batches of 6
batch_size = 6
batches = {}
for i in range(0, len(output), batch_size):
    batch_number = (i // batch_size) + 1
    batch_key = f"Batch{batch_number}"
    batches[batch_key] = output[i:i + batch_size]

with open('scraper/scraper/Listing_Url/json_file/final_rental_link.json', 'w') as f:
    json.dump(batches, f, indent=4)

print("Data saved to final_rental_link.json")
