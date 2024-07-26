import pandas as pd
import os
import pyodbc
import csv

# Define URL parts
URL_PREFIX = "https://www.airbnb.ca/s"
URL_MIDDLE = "homes?date_picker_type=calendar&currency=USD"


def generate_url(city, state, country, checkin, checkout, guests, bedrooms, search_range):
    url = f"{URL_PREFIX}/{city}--{state}--{country.replace(' ', '-')}/{URL_MIDDLE}&checkin={checkin}&checkout={checkout}&adults={guests}&search_mode=regular_search&min_bedrooms={bedrooms}&{search_range}"
    return url


def upload_jobs(date_file="scraper/scraper/Listing_Url/SQL_Connectors/dates.csv"):
    # Connection string from environment variable using secrets on GitHub
    connection_string = os.environ.get('SECRET_CHRISTIANSQL_STRING')

    # Establish SQL Server connection
    conn = pyodbc.connect(connection_string)
    cursor = conn.cursor()

    # Read data from InfoTable
    info_table_query = """
    SELECT [InfoID], [NumberOfBedRooms], [NumberOfGuests], [City], [State], [Country], [SearchRange]
    FROM [dbo].[InfoTable]
    """
    info_table_df = pd.read_sql(info_table_query, conn)

    # Read data from SearchRangeTable
    search_range_table_query = """
    SELECT [SearchRangeID], [SearchRangeName], [SearchRangeLocationDetails], [ScopeLevel]
    FROM [dbo].[SearchRangeTable]
    """
    search_range_table_df = pd.read_sql(search_range_table_query, conn)

    # Create a dictionary to map SearchRangeID to SearchRangeLocationDetails
    search_range_dict = search_range_table_df.set_index('SearchRangeID')['SearchRangeLocationDetails'].to_dict()

    # Read dates from dates.csv
    with open(date_file, mode='r') as file:
        csv_reader = csv.DictReader(file)
        date_records = [row for row in csv_reader]


    job_data = []
    job_id_query = "SELECT MAX(JobID) FROM [dbo].[JobTable]"
    cursor.execute(job_id_query)
    job_id = cursor.fetchone()[0] or 0

    for _, info_record in info_table_df.iterrows():
        info_id = info_record['InfoID']
        city = info_record['City']
        state = info_record['State']
        country = info_record['Country']
        guests = info_record['NumberOfGuests']
        bedrooms = info_record['NumberOfBedRooms']
        search_range_id = info_record['SearchRange']

        # Get the actual search_range location details
        search_range = search_range_dict.get(search_range_id, '')

        for date_record in date_records:
            start_date = date_record['Start Date']
            end_date = date_record['End Date']
            url = generate_url(city, state, country, start_date, end_date, guests, bedrooms, search_range)

            job_id += 1
            job_data.append((job_id, info_id, start_date, end_date, url, "PENDING"))

    # Insert data into JobTable
    insert_query = """
    INSERT INTO [dbo].[JobTable] ([JobID], [InfoID], [StartDate], [EndDate], [URL], [Status])
    VALUES (?, ?, ?, ?, ?, ?)
    """
    cursor.executemany(insert_query, job_data)
    conn.commit()

    # Close connection
    conn.close()

    print("Data inserted successfully into JobTable.")


upload_jobs()
