import pandas as pd
import json
import os
from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build
import pyodbc

# Constants
SHEET_ID = '10OgYeu7oj5Lwtr4gGy14zXuZlAk0gibSbgq_AmUtf7Q'
JobTable = 'JobTable_Results'
GOOGLE_SHEETS_CREDENTIALS = os.getenv("GOOGLE_SHEETS_CREDENTIALS")
TABLE_NAME = 'ResultSummary'  # Replace with your actual table name

# Google Sheets API credentials
credentials = Credentials.from_service_account_info(json.loads(GOOGLE_SHEETS_CREDENTIALS))

# Google Sheets API service
service = build("sheets", "v4", credentials=credentials)

# Read data from Google Sheets
sheet = service.spreadsheets()
result = sheet.values().get(spreadsheetId=SHEET_ID, range=JobTable).execute()
values = result.get('values', [])

# Convert data to DataFrame
df = pd.DataFrame(values[1:], columns=values[0])

# Ensure numeric columns are converted to appropriate types
numeric_columns = [
    'JobID', 'InfoID', 'rank', 'orig_price_per_night', 'cleaning_fee', 'service_fee',
    'total_price', 'price_per_night'
]
df[numeric_columns] = df[numeric_columns].apply(pd.to_numeric, errors='coerce')

# Perform calculations for the summary statistics
summary = df.groupby('JobID').agg(
    OrigPricePerNight_mean=('orig_price_per_night', 'mean'),
    OrigPricePerNight_median=('orig_price_per_night', 'median'),
    OrigPricePerNight_max=('orig_price_per_night', 'max'),
    OrigPricePerNight_min=('orig_price_per_night', 'min'),
    CleaningFee_mean=('cleaning_fee', 'mean'),
    CleaningFee_median=('cleaning_fee', 'median'),
    CleaningFee_max=('cleaning_fee', 'max'),
    CleaningFee_min=('cleaning_fee', 'min'),
    ServiceFee_mean=('service_fee', 'mean'),
    ServiceFee_median=('service_fee', 'median'),
    ServiceFee_max=('service_fee', 'max'),
    ServiceFee_min=('service_fee', 'min'),
    TotalPrice_mean=('total_price', 'mean'),
    TotalPrice_median=('total_price', 'median'),
    TotalPrice_max=('total_price', 'max'),
    TotalPrice_min=('total_price', 'min'),
    PricePerNight_mean=('price_per_night', 'mean'),
    PricePerNight_median=('price_per_night', 'median'),
    PricePerNight_max=('price_per_night', 'max'),
    PricePerNight_min=('price_per_night', 'min')
).reset_index()

# Add Run_Date column to the summary DataFrame
summary['Run_Date'] = pd.to_datetime(df['Run_Date'].iloc[0])

# Connection string from environment variable
connection_string = os.environ.get('SECRET_CHRISTIANSQL_STRING')

# Establish SQL Server connection
conn = pyodbc.connect(connection_string)
cursor = conn.cursor()

# Insert DataFrame data into SQL Server table
insert_query = f"""
INSERT INTO {TABLE_NAME} (
    JobID, OrigPricePerNight_mean, OrigPricePerNight_median, OrigPricePerNight_max, OrigPricePerNight_min,
    CleaningFee_mean, CleaningFee_median, CleaningFee_max, CleaningFee_min, ServiceFee_mean, ServiceFee_median,
    ServiceFee_max, ServiceFee_min, TotalPrice_mean, TotalPrice_median, TotalPrice_max, TotalPrice_min,
    PricePerNight_mean, PricePerNight_median, PricePerNight_max, PricePerNight_min, Run_Date
) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
"""

# Execute insert queries
for index, row in summary.iterrows():
    cursor.execute(insert_query, row.tolist())

# Commit the transaction
conn.commit()

# Close the connection
cursor.close()
conn.close()

print("Data inserted successfully into the SQL Server table.")
