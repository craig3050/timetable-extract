from bs4 import BeautifulSoup
import csv

# Read HTML data from the text file
with open('timetable_data_Lizzy.txt', 'r') as html_file:
    html_data = html_file.read()

# Parse the HTML content
soup = BeautifulSoup(html_data, 'html.parser')

# Initialize a list to store extracted data
data_list = []

# Find all elements with class "mis-cal-text"
entries = soup.find_all('div', class_='mis-cal-text')

# Loop through the entries and extract data
for entry in entries:
    # Find the nearest preceding 'td' element with 'data-datetime' attribute
    td = entry.find_previous('td', {'data-datetime': True})
    
    if td:
        date = td['data-datetime'].split()[0]
    else:
        date = None  # Handle the case when the date is not found

    event_id = entry['data-eventid']
    time, class_info = entry.text.split(' ', 1)
    data_list.append({'Date': date, 'Event ID': event_id, 'Time': time, 'Class': class_info})

# Write the extracted data to a CSV file
with open('output.csv', 'w', newline='') as csvfile:
    fieldnames = ['Date', 'Event ID', 'Time', 'Class']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

    writer.writeheader()
    for row in data_list:
        writer.writerow(row)

print("Data extracted and saved to 'output.csv'.")
