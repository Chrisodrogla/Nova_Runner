import json
from datetime import datetime

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
        "currency":"USD"
    }

    params_string = '&'.join([f"{key}={value}" for key, value in params.items()])
    listing_link = f"{base_url}?{params_string}"

    return listing_link


# jSON data from file
with open('listing_attribute.json', 'r') as f:
    listings = json.load(f)

# Date Ranges
start_date_str = '2024-05-21'
end_date_str = '2024-05-25'
start_date = datetime.strptime(start_date_str, "%Y-%m-%d").date()
end_date = datetime.strptime(end_date_str, "%Y-%m-%d").date()
delta_days = (end_date - start_date).days

output = []

for listing in listings:
    address = listing["address"]
    guest = listing["guest"]
    baths = listing["baths"]
    beds = listing["beds"]
    bedrooms = listing["bedrooms"]
    rankbreeze_Id = listing["rankbreeze_Id"]
    airbnb_link = listing["airbnb_link"]
    listing_link = generate_listing_link(address, start_date_str, end_date_str, delta_days, guest, bedrooms, beds,
                                         baths)

    rental_id = airbnb_link.replace("https://www.airbnb.com/rooms/", "")

    output_entry = {
        "listing_link_format": listing_link,
        "rankbreeze_Id": rankbreeze_Id,
        "rental_id": rental_id
    }

    output.append(output_entry)

with open('final_rental_link.json', 'w') as f:
    json.dump(output, f, indent=4)

print("Data on Json")
