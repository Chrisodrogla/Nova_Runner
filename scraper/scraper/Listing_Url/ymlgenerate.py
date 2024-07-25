import os

# Define the range of file numbers
start = 1

end = 108


# Directory where the files will be created
directory = r"C:\Users\calgo\Github_vscode_Cloned\Nova_Runner\.github\workflows"

# Create the directory if it doesn't exist
os.makedirs(directory, exist_ok=True)

# Template for the YAML content
template = """name: Run Batch {batch_number}

on:
  workflow_dispatch:
  schedule:
    - cron: "40 7 * * *" # 11:40 AM PH time
jobs:
  run-scraper:
    runs-on: ubuntu-latest

    steps:
    - name: Checkout repository
      uses: actions/checkout@v2

    - name: Set up Python
      uses: actions/setup-python@v2
      with:
        python-version: '3.8'

    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install -r requirements.txt
        pip install gspread oauth2client pandas gspread-dataframe
        pip install google-auth google-auth-oauthlib google-auth-httplib2 google-api-python-client

    - name: Run scraper script
      env:
        GOOGLE_SHEETS_CREDENTIALS: ${{{{ secrets.GOOGLE_SHEETS_CREDENTIALS }}}}

      run: |
        BATCH_ID=Batch{batch_number} python scraper/scraper/Listing_Url/simultaneous.py
"""

# Generate the files
for i in range(start, end + 1):
    filename = f"Scrape_Runner_{i}.yml"
    filepath = os.path.join(directory, filename)
    content = template.format(batch_number=i)
    with open(filepath, 'w') as file:
        file.write(content)

print(f"Created {end - start + 1} YAML files in {directory}")
