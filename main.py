from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
import requests
import os

# Initialize
bot = os.environ['TELEGRAM_BOT_TOKEN']
chat_id = os.environ['TELEGRAM_CHANNEL_ID']
url = os.environ['URL']
high_events = ""
all_events = ""

# Path to the ChromeDriver executable
chromedriver_path = '/path/to/chromedriver'

# Set Chrome options to run in headless mode
chrome_options = Options()
chrome_options.add_argument('--headless')  # Run Chrome in headless mode

# Start the ChromeDriver service
service = Service(chromedriver_path)

# Start the WebDriver
driver = webdriver.Chrome(service=service, options=chrome_options)

# Load the webpage
# timezone = 27 = GMT+8
driver.get(url)

# Wait for the table to load (adjust the wait time as needed)
driver.implicitly_wait(10)

# Find the table element
table = driver.find_element(By.ID, 'ecEventsTable')

# Find all the event rows in the table
event_rows = table.find_elements(By.TAG_NAME, 'tr')

# Iterate over the event rows and print the event details
for event_row in event_rows:
    cells = event_row.find_elements(By.TAG_NAME, 'td')
    if len(cells) >= 8:
        time = cells[0].text.strip()
        currency = cells[1].text.strip()
        sentiment = cells[2].get_attribute('title')
        event = cells[3].text.strip()
        actual = cells[4].text.strip()
        forecast = cells[5].text.strip()
        previous = cells[6].text.strip()

        if "High Volatility Expected" in sentiment:
            high_events += "Time: {time}\nCurrency: {currency}\nImportance: {sentiment}\nEvent: {event}\nForecast: {forecast}\nPrevious: {previous}\n\n"
         
        all_events += f"Time: {time}\nCurrency: {currency}\nImportance: {sentiment}\nEvent: {event}\nActual: {actual}\nForecast: {forecast}\nPrevious: {previous}\n\n"

message = f"Daily Forex News Alert - High Impact - SGT\n{high_events}\n[all news for today]({url})"

requests.get(
    f"https://api.telegram.org/{bot}/sendMessage?chat_id={chat_id}&text="
    + f"{message}"
    + "&parse_mode=markdown&disable_web_page_preview=True"
)

print(all_events)
# Close the WebDriver
driver.quit()
