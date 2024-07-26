import csv
from datetime import datetime, timedelta

# This function generates dates of Monday to Thursday every week for the next 3 months and save to a csv file
def generate_regular_dates():
    # Get the current date
    current_date = datetime.now()
    
    # Find the next Monday
    next_monday = current_date + timedelta(days=(7 - current_date.weekday()) % 7)
    
    # Generate dates for the next 3 months (approximately 13 weeks)
    end_date = current_date + timedelta(weeks=13)
    
    dates = []
    while next_monday < end_date:
        start_date = next_monday
        thursday_date = start_date + timedelta(days=3)  # Thursday
        
        dates.append([start_date.strftime('%Y-%m-%d'), thursday_date.strftime('%Y-%m-%d')])
        
        # Move to the next Monday
        next_monday += timedelta(days=7)
    
    return dates

def save_to_csv(dates, filename='dates.csv'):
    # Define the header
    header = ['Start Date', 'End Date']
    
    # Write data to CSV
    with open(filename, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(header)
        writer.writerows(dates)

# Generate the dates
dates = generate_regular_dates()

# Save dates to a CSV file
save_to_csv(dates)