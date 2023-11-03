from selenium import webdriver
from selenium.webdriver.common.by import By
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
from undetected_chromedriver import Chrome, ChromeOptions
import csv
import time
import datetime
import argparse
import random
from paho.mqtt import client as mqtt_client
import json

# MQTT Setup
broker = "192.168.0.14"
port = 1883
topic = "python/mqtt"
# Generate a Client ID with the publish prefix.
client_id = f'publish-{random.randint(0, 1000)}'
username_mqtt = 'craig'
password_mqtt = 'revaeb'


# Create a parser object
parser = argparse.ArgumentParser(description="A script that takes username, password, and login URL as arguments.")

# Add arguments to the parser
parser.add_argument("username", type=str, help="Your username")
parser.add_argument("password", type=str, help="Your password")
parser.add_argument("login_url", type=str, help="The URL for login")

# Parse the command-line arguments
args = parser.parse_args()

# Now you can access the arguments as attributes of the 'args' object
username = args.username
password = args.password
login_url = args.login_url

def request_info():
    try:
        # Set up the ChromeOptions with undetected-chromedriver
        chrome_options = ChromeOptions()
        chrome_options.add_argument('--headless')  # Run Chrome in headless mode (no GUI)
        chrome_options.add_argument('--disable-extensions')
        chrome_options.add_argument('--disable-infobars')
        chrome_options.add_argument('--disable-popup-blocking')

        # Create a WebDriver with undetected-chromedriver
        driver = webdriver.Chrome()

        # Navigate to the login page
        driver.get(login_url)

        time.sleep(2)

        # Find and fill in the username and password fields
        username_field = driver.find_element(By.ID, "username")  # Change to the actual username field name
        password_field = driver.find_element(By.ID, "password")  # Change to the actual password field name

        username_field.send_keys(username)
        password_field.send_keys(password)

        # Submit the form to log in
        password_field.submit()

        # Wait for the page to load, you can adjust the sleep time as needed
        time.sleep(2)  # Adjust the sleep duration as needed

        # Get the page source after logging in
        page_source = driver.page_source

        # Parse the page source using BeautifulSoup
        soup = BeautifulSoup(page_source, 'html.parser')

        # Find all <li> elements with the specified class name
        items = soup.find_all('li', class_='calendar-widget-item')

        # Create lists to store the extracted data
        dates = []
        titles = []
        locations = []

        today = datetime.date.today()

        # Create empty dictionary for returned values
        return_dict = {}

        for item in items:
            try:
                # Extract the title
                try:
                    title = item.find('span', {'class': 'calendar-widget-item-title'}).text
                except AttributeError:
                    title = "??"

                # Extract the location
                try:
                    location = item.find('span', {'class': 'calendar-widget-item-location'}).text
                except AttributeError:
                    location = "??"

                # Extract the date
                try:
                    date = item.find('span', {'class': 'calendar-widget-item-date'}).text
                except AttributeError:
                    date = "??"

                print(f"Title: {title}")
                print(f"Location: {location}")
                print(f"Date: {date}")
                return_dict[date] = [title, location]

            except Exception as e:
                print(f"An error occurred: {str(e)}")

        attendance = soup.find('div', {'class': 'mis-htmlpanel-measure-value'}).text
        positive_recognition = soup.find('div', class_='mis-htmlpanel-measure-value', style='color:#7bbc3a').text
        print(f"Attendance: {attendance}")
        print(f"Positive Recognition: {positive_recognition}")
        return_dict["Attendance"] = attendance
        return_dict["Positive Recognition"] = positive_recognition

        # Write the elements to a text file
        with open(f'{today} - Export.txt', 'w') as file:
            json.dump(return_dict, file)

        print("Data has been written to Export.txt")

        return return_dict

    except Exception as e:
        print(f"An error occurred: {str(e)}")

    finally:
        if 'driver' in locals():
            driver.quit()


def connect_mqtt():
    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            print("Connected to MQTT Broker!")
        else:
            print("Failed to connect, return code %d\n", rc)

    client = mqtt_client.Client(client_id)
    client.username_pw_set(username_mqtt, password_mqtt)
    client.on_connect = on_connect
    client.connect(broker, port)
    return client


def publish(client, message):
    msg = f"messages: {message}"
    result = client.publish(topic, msg)
    status = result[0]
    if status == 0:
        print(f"Send `{msg}` to topic `{topic}`")
    else:
        print(f"Failed to send message to topic {topic}")



def run():
    requested_info = request_info()
    requested_info_json = json.dumps(requested_info)
    print(f'Info to send: {requested_info_json}')
    client = connect_mqtt()
    client.loop_start()
    publish(client, requested_info_json)
    client.loop_stop()


if __name__ == '__main__':
    run()