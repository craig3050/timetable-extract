from selenium import webdriver
from bs4 import BeautifulSoup
from undetected_chromedriver import Chrome, ChromeOptions

# Specify the URL of the website you want to log in to
login_url = ""

# Specify your username and password
username = ""
password = ""

# Set up the ChromeOptions with undetected-chromedriver
chrome_options = ChromeOptions()
chrome_options.add_argument('--headless')  # Run Chrome in headless mode (no GUI)
chrome_options.add_argument('--disable-extensions')
chrome_options.add_argument('--disable-infobars')
chrome_options.add_argument('--disable-popup-blocking')

# Create a WebDriver with undetected-chromedriver
driver = Chrome(options=chrome_options)

# Navigate to the login page
driver.get(login_url)

# Find and fill in the username and password fields
username_field = driver.find_element_by_name("username")  # Change to the actual username field name or ID
password_field = driver.find_element_by_name("password")  # Change to the actual password field name or ID

username_field.send_keys(username)
password_field.send_keys(password)

# Submit the form to log in
password_field.submit()

# Wait for the page to load, you can adjust the sleep time as needed
import time
time.sleep(5)  # Adjust the sleep duration as needed

# Get the page source after logging in
page_source = driver.page_source

# Parse the page source using BeautifulSoup
soup = BeautifulSoup(page_source, 'html.parser')

# Find the outer span element with the class "calendar-widget-item-link"
item = soup.find('span', class_='calendar-widget-item-link')

# Extract the title, location, and date
title = item.find('span', {'class': 'calendar-widget-item-title'}).text
location = item.find('span', {'class': 'calendar-widget-item-location'}).text
date = item.find('span', {'class': 'calendar-widget-item-date'}).text

# Find the "Attendance" value
attendance = soup.find('div', {'class': 'mis-htmlpanel-measure-value'}).text

# Find the "Positive Recognition" value
positive_recognition = soup.find('div', {'class': 'mis-htmlpanel-measure-value'}).text



print(f"Title: {title}")
print(f"Location: {location}")
print(f"Date: {date}")

# Define the CSV filename
csv_filename = 'data.csv'

# Write the data to a CSV file
with open(csv_filename, 'w', newline='') as csvfile:
    csv_writer = csv.writer(csvfile)
    
    # Write the header row
    csv_writer.writerow(['Title', 'Location', 'Date', 'Attendance', 'positive_recognition'])
    
    # Write the extracted data
    csv_writer.writerow([title, location, date, attendance, positive_recognition])

print(f"Data has been written to {csv_filename}")



# Don't forget to close the WebDriver when you're done
driver.quit()
