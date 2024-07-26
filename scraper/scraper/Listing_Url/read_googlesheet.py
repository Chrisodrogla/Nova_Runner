import pandas as pd
import json
import os
import pyodbc
from datetime import datetime

# Connection string from environment variable using secrets on GitHub
connection_string = os.environ.get('SECRET_CHRISTIANSQL_STRING')

# Establish SQL Server connection
conn = pyodbc.connect(connection_string)
cursor = conn.cursor()

# SQL query to fetch data from JobTable
query = "SELECT JobID, InfoID, StartDate, EndDate, URL, Status FROM JobTable"

# Read data from SQL Server
df = pd.read_sql(query, conn)

# Debugging: print out the column names to verify
print("Column names in DataFrame:", df.columns.tolist())

# Ensure column names are correct
expected_columns = ['JobID', 'InfoID', 'StartDate', 'EndDate', 'URL', 'Status']
missing_columns = [col for col in expected_columns if col not in df.columns]

if missing_columns:
    print(f"Missing columns in DataFrame: {missing_columns}")
    sys.exit(1)

# Get current date
current_date = datetime.now()

# Generate JSON format
data = {}
batch_size = 3
batch_number = 1

for i in range(0, len(df), batch_size):
    batch = df.iloc[i:i+batch_size]
    batch_key = f"Batch{batch_number}"
    data[batch_key] = []
    for _, row in batch.iterrows():
        start_date = datetime.strptime(row['StartDate'], '%Y-%m-%d')  # Adjust the date format if necessary
        if row['Status'] == 'PASSED' or start_date < current_date:
            # Update Status to 'PASSED' if the start date is in the past and it's not already 'PASSED'
            if row['Status'] != 'PASSED' and start_date < current_date:
                update_query = f"UPDATE JobTable SET Status = 'PASSED' WHERE JobID = {row['JobID']}"
                cursor.execute(update_query)
                conn.commit()
            continue
        data[batch_key].append({
            "listing_link_format": row['URL'],
            "JobID": row['JobID'],
            "InfoID": row['InfoID']
        })
    batch_number += 1

# Save JSON to file
searchjobtable_file_path = 'scraper/scraper/Listing_Url/json_file/final_rental_link.json'
with open(searchjobtable_file_path, 'w') as json_file:
    json.dump(data, json_file, indent=4)

print(f"JSON data saved to {searchjobtable_file_path}")

# Close the SQL Server connection
conn.close()
