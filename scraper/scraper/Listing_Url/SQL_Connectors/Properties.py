import pandas as pd
import json
import os
from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build
import pyodbc

SHEET_ID = '10OgYeu7oj5Lwtr4gGy14zXuZlAk0gibSbgq_AmUtf7Q'
PROPERTIES_TABLE = 'Properties'
GOOGLE_SHEETS_CREDENTIALS = os.getenv("GOOGLE_SHEETS_CREDENTIALS")
credentials = Credentials.from_service_account_info(json.loads(GOOGLE_SHEETS_CREDENTIALS))


service = build("sheets", "v4", credentials=credentials)


sheet = service.spreadsheets()
result = sheet.values().get(spreadsheetId=SHEET_ID, range=PROPERTIES_TABLE).execute()
values = result.get('values', [])

df = pd.DataFrame(values[1:], columns=values[0])

print("Column names in DataFrame:", df.columns.tolist())


df.columns = ['PropertyID', 'PropertyName', 'InfoID', 'HostName', 'CoHostName', 'NumberOfBedRooms', 'NumberOfBathrooms', 'NumberOfGuests', 'ResortName', 'City', 'State', 'Country', 'SearchRange', 'MainListingID']


df['PropertyID'] = df['PropertyID'].astype(str)
df['PropertyName'] = df['PropertyName'].astype(str)
df['InfoID'] = df['InfoID'].astype(str)
df['HostName'] = df['HostName'].astype(str)
df['CoHostName'] = df['CoHostName'].astype(str)
df['NumberOfBedRooms'] = df['NumberOfBedRooms'].astype(float)  # Use float in case there are decimals
df['NumberOfBathrooms'] = df['NumberOfBathrooms'].astype(float)  # Already float
df['NumberOfGuests'] = df['NumberOfGuests'].astype(float)  # Use float in case there are decimals
df['ResortName'] = df['ResortName'].astype(str)
df['City'] = df['City'].astype(str)
df['State'] = df['State'].astype(str)
df['Country'] = df['Country'].astype(str)
df['SearchRange'] = df['SearchRange'].astype(float)  # Use float in case there are decimals
df['MainListingID'] = df['MainListingID'].astype(str)


connection_string = os.environ.get('SECRET_CHRISTIANSQL_STRING')


conn = pyodbc.connect(connection_string)
cursor = conn.cursor()

batch_size = 100000
for start in range(0, len(df), batch_size):
    batch = df.iloc[start:start+batch_size]
    for index, row in batch.iterrows():
        cursor.execute("""
            INSERT INTO Properties (PropertyID, PropertyName, InfoID, HostName, CoHostName, NumberOfBedRooms, NumberOfBathrooms, NumberOfGuests, ResortName, City, State, Country, SearchRange, MainListingID)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, row['PropertyID'], row['PropertyName'], row['InfoID'], row['HostName'], row['CoHostName'], row['NumberOfBedRooms'], row['NumberOfBathrooms'], row['NumberOfGuests'], row['ResortName'], row['City'], row['State'], row['Country'], row['SearchRange'], row['MainListingID'])
    conn.commit()


conn.close()
