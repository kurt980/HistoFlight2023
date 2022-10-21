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

today = date.today()
daysAhead = 60
flightProps = ['nonstop', 'one way']
classOptions = ['economy']
cities = ['ORD', 'LAX', 'SFO']
baseUrl = 'https://www.google.com/travel/flights?q=Flights'

def clickButton(button):
    try:
        button.click()
        return True
    except:
        return False

def expandDetails(buttons, interval):
    for button in buttons:
        errorCounter = 0
        while not clickButton(button):
            errorCounter += 1
            print('Retry expanding a field')
            if errorCounter == 10:
                print('Expand failed')
                return False
            time.sleep(interval)
        time.sleep(interval)
    return True

def scrapeData(url):
    WINDOW_SIZE = "1920,1080"

    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--window-size=%s" % WINDOW_SIZE)

    driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), chrome_options=chrome_options)
    print('Crawling from ' + url)
    driver.get(url)

    WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.CLASS_NAME, "YMlIz"))
    )
    print('Page opened')

    buttons = driver.find_elements(By.XPATH, ".//button[contains(@aria-label, 'Flight details')]")

    print('Expanding flight details')
    CLICK_INTERVAL = 0.2
    while not expandDetails(buttons, CLICK_INTERVAL):
        print('Retry crawling from ' + url)
        driver.get(url)

        WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.CLASS_NAME, "YMlIz"))
        )
        print('Page opened')

        buttons = driver.find_elements(By.XPATH, ".//button[contains(@aria-label, 'Flight details')]")
        
        CLICK_INTERVAL += 0.2
        
    elements = driver.find_elements(By.XPATH, "//div[@role='main']//li[@class='pIav2d']")

    data = []
    for el in elements:
        data.append(el.text)

    driver.quit()
    return data


for departCity in cities:
    for arrivalCity in cities:
        if departCity == arrivalCity:
            continue

        for timeDiff in range(1, daysAhead + 1):
            flightDate = today + timedelta(days=timeDiff)
            for flightClass in classOptions:
                queryUrl = ' from ' + departCity + ' to ' + arrivalCity + ' on ' + str(flightDate) + ' ' + ' '.join(flightProps) + ' ' + flightClass
                url = baseUrl + quote(queryUrl)

                data = scrapeData(url)
                
                outF = open("flight_data.txt", "a")
        
                print('Writing data to file')

                for datum in data:
                    outF.write("Ticket Date: ")
                    outF.write(today.strftime("%m-%d-%Y\n"))
                    outF.write("Departure Date: ")
                    outF.write(flightDate.strftime("%m-%d-%Y\n"))
                    outF.write(datum)
                    outF.write("\n\nseperator\n\n")

                outF.close()
                print('Stored data to file')
