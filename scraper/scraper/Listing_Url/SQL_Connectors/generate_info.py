import pandas as pd
import os
import pyodbc

# Connection string from environment variable using secrets on github
connection_string = os.environ.get('SECRET_CHRISTIANSQL_STRING')

# Establish SQL Server connection
conn = pyodbc.connect(connection_string)
cursor = conn.cursor()

# Query to read all data from the Properties table
properties_query = """
SELECT [PropertyID], [PropertyName], [InfoID], [HostName], [CoHostName], 
       [NumberOfBedRooms], [NumberOfBathrooms], [NumberOfGuests], 
       [ResortName], [City], [State], [Country], [SearchRange], [MainListingID]
FROM [dbo].[Properties]
"""

# Read data from Properties table into a DataFrame
properties_df = pd.read_sql(properties_query, conn)

# Extract unique properties information
unique_properties = properties_df[['NumberOfBedRooms', 'NumberOfGuests', 'City', 'State', 'Country', 'SearchRange']].drop_duplicates()

# Query to read all data from the InfoTable table
info_table_query = """
SELECT [InfoID], [NumberOfBedRooms], [NumberOfGuests], [City], [State], [Country], [SearchRange]
FROM [dbo].[InfoTable]
"""

# Read data from InfoTable table into a DataFrame
info_table_df = pd.read_sql(info_table_query, conn)

# Get existing InfoIDs to determine the next unique InfoID
existing_info_ids = info_table_df['InfoID'].tolist()

# Determine the starting point for the next unique InfoID
if existing_info_ids:
    next_info_id = max(existing_info_ids) + 1
else:
    next_info_id = 1

# Prepare data for insertion
data_to_insert = []
info_mapping = {}  # Dictionary to map unique properties to their InfoID
for _, row in unique_properties.iterrows():
    data_to_insert.append((next_info_id, row['NumberOfBedRooms'], row['NumberOfGuests'], row['City'], row['State'], row['Country'], row['SearchRange']))
    info_mapping[(row['NumberOfBedRooms'], row['NumberOfGuests'], row['City'], row['State'], row['Country'], row['SearchRange'])] = next_info_id
    next_info_id += 1

# Insert data into InfoTable
insert_query = """
INSERT INTO [dbo].[InfoTable] ([InfoID], [NumberOfBedRooms], [NumberOfGuests], [City], [State], [Country], [SearchRange])
VALUES (?, ?, ?, ?, ?, ?, ?)
"""

cursor.executemany(insert_query, data_to_insert)
conn.commit()

# Update InfoID in Properties table
for index, row in properties_df.iterrows():
    property_tuple = (row['NumberOfBedRooms'], row['NumberOfGuests'], row['City'], row['State'], row['Country'], row['SearchRange'])
    if property_tuple in info_mapping:
        properties_df.at[index, 'InfoID'] = info_mapping[property_tuple]

# Update the Properties table with the new InfoID values
update_query = """
UPDATE [dbo].[Properties]
SET InfoID = ?
WHERE PropertyID = ?
"""

update_data = properties_df[['InfoID', 'PropertyID']].values.tolist()
cursor.executemany(update_query, update_data)
conn.commit()

# Close connection
conn.close()

print("Data inserted successfully into InfoTable and Properties table updated.")
