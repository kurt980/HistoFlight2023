import os
import time
from datetime import date, timedelta
from urllib.parse import quote

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager

today = date.today()
daysAhead = 3
flightProps = ['nonstop', 'one way']
classOptions = ['economy']
cities = ['ORD', 'LAX', 'SFO']
baseUrl = 'https://www.google.com/travel/flights?q=Flights'
dataPath = '../HistoFlight2023/data/raw/' + today.strftime(("%Y.%m.%d"))

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

    '''
    To determine the correct XPATH expression to use, you would need to inspect the HTML source code of the webpage and locate the specific element 
    that contains the flight details information you are interested in.

    One approach is to use the browser's developer tools, which typically include an "Inspector" or "Elements" panel that displays the HTML structure 
    of the page. You can then use the Inspector to select the element that contains the flight details information and view its attributes and properties to help you construct the appropriate XPATH expression.

    Another approach is to manually scan the HTML source code of the page for relevant tags and attributes that may indicate the location of the flight 
    details information. For example, you might look for class names or data attributes that are associated with the flight details section of the page. 
    Once you have identified the appropriate element(s), you can construct an XPATH expression that targets them specifically.
    '''

    data = []
    for el in elements:
        data.append(el.text)

    driver.quit()
    return data

if not os.path.isdir(dataPath):
   os.makedirs(dataPath)

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
                
                outF = open(dataPath + "/flight_data.txt", "a", encoding="utf-8")
        
                print('Writing data to file')

                for datum in data:
                    outF.write("Ticket Date: ")
                    outF.write(today.strftime("%m-%d-%Y\n"))
                    outF.write("Departure Date: ")
                    outF.write(flightDate.strftime("%m-%d-%Y\n"))
                    outF.write(datum) # Error is here
                    outF.write("\n\nseperator\n\n")

                outF.close()
                print('Stored data to file')