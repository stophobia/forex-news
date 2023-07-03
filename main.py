from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
import requests
import telegram
import os

# Initialize Telegram bot
bot = os.environ['TELEGRAM_BOT_TOKEN'])
chat_id = os.environ['TELEGRAM_CHANNEL_ID']
high_events = ""

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
url = 'https://ec.forexprostools.com/?columns=exc_currency,exc_importance&importance=1,2,3&calType=day&timeZone=27&lang=1'
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
    if len(cells) >= 4:
        time = cells[0].text.strip()
        currency = cells[1].text.strip()
        sentiment = cells[2].get_attribute('title') or ''
        event = cells[3].text.strip()

        if "High Volatility Expected" in sentiment:
            high_events += f"Time: {time} | Currency: {currency} | Importance: {sentiment} | Event: {event}\n"
            
requests.get(
    f"https://api.telegram.org/{bot}/sendMessage?chat_id={chat_id}&text="
    + f"{high_events}"
    + "&parse_mode=markdown&disable_web_page_preview=True"
)
print(high_events)
# Close the WebDriver
driver.quit()


