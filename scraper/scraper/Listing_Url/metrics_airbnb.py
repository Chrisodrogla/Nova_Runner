import os
import shutil
import pandas as pd
import requests
import json

# Step 1: Define API credentials
TOKEN_KEY = os.getenv("TOKEN_KEY")
TOKEN_SECRET = os.getenv("TOKEN_SECRET")


# Step 2: Define the API endpoint
api_url = "https://web.streamlinevrs.com/api/json"

# Step 3: Create the request payload
payload = {
    "methodName": "GetPropertyInfo",
    "params": {
        "token_key": TOKEN_KEY,
        "token_secret": TOKEN_SECRET,
        "unit_id": 575257,
        "return_multiple_housekeepers": 1,
        "include_owners": 1,
        "owner_manager": 1,
        "maintenance_plan": 1,
        "unit_proposition_package": 1,
        "return_markup": 1,
        "show_advance_date": 1,
        "show_website_url": 1,
        "show_wifi_name": 1,
        "show_housekeeping_status": 1
    }
}

# Step 4: Send the POST request to the API
response = requests.post(api_url, json=payload)

# Step 5: Print the response
if response.status_code == 200:
    # Print the JSON response in a formatted way
    result = response.json()
    print(json.dumps(result, indent=4))
else:
    print(f"Error: {response.status_code}, {response.text}")
 
