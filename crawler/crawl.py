from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager

from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from datetime import date
from datetime import timedelta

import time

from urllib.parse import quote

CLICK_INTERVAL = 0.2

def clickButton(button):
    try:
        button.click()
        return True
    except:
        print('button click failed')
        return False

def scrapeData(url):
    WINDOW_SIZE = "1920,1080"

    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--window-size=%s" % WINDOW_SIZE)

    driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), chrome_options=chrome_options)
    print('crawling from ' + url)
    driver.get(url)

    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CLASS_NAME, "YMlIz"))
    )
    print('Page opened')

    elements = driver.find_elements(By.XPATH, "//div[@role='main']//li[not(@role='option')]")
    buttons = driver.find_elements(By.XPATH, ".//button[contains(@aria-label, 'Flight details')]")

    print('Expanding flight details')
    for button in buttons:
        while (not clickButton(button)):
            time.sleep(CLICK_INTERVAL)
        time.sleep(CLICK_INTERVAL)
    
    outF = open("flight_data.txt", "a")
    
    print('Writing data to file')
    for el in elements:
        outF.write(el.text)
        outF.write('\n\nseperator\n\n')

    driver.quit()
    outF.close()
    print('Stored data to file')

today = date.today()
daysAhead = 1
flightProps = ['nonstop', 'one way']
cities = ['ORD', 'LAX', 'SFO']
baseUrl = 'https://www.google.com/travel/flights?q=Flights'
for i in range(len(cities)):
    for j in range(i + 1, len(cities)):
        departCity = cities[i]
        arrivalCity = cities[j]

        for timeDiff in range(1, daysAhead + 1):
            flightDate = today + timedelta(days=timeDiff)
            queryUrl = ' from ' + departCity + ' to ' + arrivalCity + ' on ' + str(flightDate) + ' ' + ' '.join(flightProps)
            url = baseUrl + quote(queryUrl)
            scrapeData(url)


