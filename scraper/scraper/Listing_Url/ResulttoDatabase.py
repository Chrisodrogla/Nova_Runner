import pandas as pd
import json
import os
from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build
import pyodbc

# Google Sheets details
SHEET_ID = '18qCzoA5vi0EKlBf1s8sgC8F1NhSLxD_7L2rNAQcOkVY'
PROPERTIES_RANGE = 'Properties'
LISTINGS_RANGE = 'Listings'
GOOGLE_SHEETS_CREDENTIALS = os.getenv("GOOGLE_SHEETS_CREDENTIALS")


credentials = Credentials.from_service_account_info(json.loads(GOOGLE_SHEETS_CREDENTIALS))

service = build("sheets", "v4", credentials=credentials)


def read_sheet_data(sheet_id, range_name):
    sheet = service.spreadsheets()
    result = sheet.values().get(spreadsheetId=sheet_id, range=range_name).execute()
    values = result.get('values', [])
    if not values:
        return pd.DataFrame()
    return pd.DataFrame(values[1:], columns=values[0])



properties_df = read_sheet_data(SHEET_ID, PROPERTIES_RANGE)
listings_df = read_sheet_data(SHEET_ID, LISTINGS_RANGE)


connection_string = os.environ.get('SECRET_CHRISTIANSQL_STRING')

conn = pyodbc.connect(connection_string)
cursor = conn.cursor()


def insert_data_to_sql(table_name, df):
    columns = ', '.join(df.columns)
    placeholders = ', '.join(['?'] * len(df.columns))
    insert_query = f"INSERT INTO {table_name} ({columns}) VALUES ({placeholders})"

    for row in df.itertuples(index=False, name=None):
        cursor.execute(insert_query, row)

    conn.commit()



insert_data_to_sql('Properties', properties_df)


insert_data_to_sql('Listings', listings_df)

conn.close()
