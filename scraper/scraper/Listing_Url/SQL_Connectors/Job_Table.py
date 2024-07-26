import pandas as pd
import json
import os
from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build
import pyodbc

# Google Sheets and SQL Server configurations

SHEET_ID = '18qCzoA5vi0EKlBf1s8sgC8F1NhSLxD_7L2rNAQcOkVY'
SHEET_NAME = 'JobTable'
GOOGLE_SHEETS_CREDENTIALS = os.getenv("GOOGLE_SHEETS_CREDENTIALS")
credentials = Credentials.from_service_account_info(json.loads(GOOGLE_SHEETS_CREDENTIALS))

# Google Sheets API service
service = build("sheets", "v4", credentials=credentials)
sheet = service.spreadsheets()
result = sheet.values().get(spreadsheetId=SHEET_ID, range=SHEET_NAME).execute()
values = result.get('values', [])

# Convert to DataFrame
df = pd.DataFrame(values[1:], columns=values[0])


print("Column names in DataFrame:", df.columns.tolist())
df.columns = ['JobID', 'InfoID', 'StartDate', 'EndDate', 'URL', 'Status']

# Convert data types to match SQL table
df['JobID'] = df['JobID'].astype(int)
df['InfoID'] = df['InfoID'].astype(int)
df['StartDate'] = pd.to_datetime(df['StartDate'], errors='coerce')
df['EndDate'] = pd.to_datetime(df['EndDate'], errors='coerce')
df['URL'] = df['URL'].astype(str)
df['Status'] = df['Status'].astype(str)


connection_string = os.environ.get('SECRET_CHRISTIANSQL_STRING')

# this will connect to sql server
conn = pyodbc.connect(connection_string)
cursor = conn.cursor()

batch_size = 100000
for start in range(0, len(df), batch_size):
    batch = df.iloc[start:start+batch_size]
    for index, row in batch.iterrows():
        cursor.execute("""
            INSERT INTO JobTable (JobID, InfoID, StartDate, EndDate, URL, Status)
            VALUES (?, ?, ?, ?, ?, ?)
        """, row['JobID'], row['InfoID'], row['StartDate'], row['EndDate'], row['URL'], row['Status'])
    conn.commit()

# Close connection
conn.close()
