import os
import time
from datetime import date, timedelta
from urllib.parse import quote

# for data processing
import csv
import hashlib
import re
from datetime import date, datetime, timedelta
from pathlib import Path
import pandas as pd

# for crawling
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager

today = date.today()
daysAhead = 2
flightProps = ['nonstop', 'one way']
classOptions = ['economy'] # currently we only crawl economy classes
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

    # FETCHING WEB DATA    
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
    # APPENDING DATA
    data = []
    for el in elements:
        data.append(el.text)

    driver.quit()
    return data
# =========================================

## PROCESSING DATE AND WRITING TO LOCAL

def processRawTicket(rawTicket):
    ticketDates = re.findall("Ticket Date: \d{1,2}-\d{1,2}-\d{4}", rawTicket)
    rawticketDate = ticketDates[0].split(" ")[-1]
    ticketDateObject = datetime.strptime(rawticketDate, "%m-%d-%Y")
    ticketDate = ticketDateObject.strftime("%Y-%m-%d")

    departureDates = re.findall("Departure Date: \d{1,2}-\d{1,2}-\d{4}", rawTicket)
    rawdepartureDate = departureDates[0].split(" ")[-1]

    # DUE TO UTF-8 ENCODING, SPACES ARE READ AS '\u202f'
    flightTimes = re.findall("(\d{1,2}:\d{1,2} [A|P]M)(\+\d+)?", rawTicket.replace('\u202f', ' '))

    print('RAW:\n', rawTicket)
    print(ticketDates, ticketDate, departureDates, flightTimes)

    # halt if no flightTimes returned
    if (len(flightTimes) == 0):
        return None

    departureTimeStr = flightTimes[0][0]
    departureTimeObject = datetime.strptime(departureTimeStr, "%I:%M %p")
    departureTime = departureTimeObject.strftime("%H:%M")

    departureDateObject = datetime.strptime(rawdepartureDate, "%m-%d-%Y")
    arrivalDateObject = departureDateObject if flightTimes[1][1] == "" else departureDateObject + timedelta(days=int(flightTimes[1][1].split("+")[-1]))

    departureDate = departureDateObject.strftime("%Y-%m-%d")
    arrivalDate = arrivalDateObject.strftime("%Y-%m-%d")
    arrivalTimeStr = flightTimes[1][0]
    arrivalTimeObject = datetime.strptime(arrivalTimeStr, "%I:%M %p")
    arrivalTime = arrivalTimeObject.strftime("%H:%M")

    travelTime = re.findall("Travel time: ((\d{1,2} hr)? ?(\d{1,2} min)?)", rawTicket)

    print('travel time')
    print('travel time', travelTime)

    if len(travelTime) == 0:
        return None
    hr = 0
    min = 0
    if travelTime[0][1] != "":
        hr = int(travelTime[0][1].split(" ")[0])
    if travelTime[0][2] != "":
        min = int(travelTime[0][2].split(" ")[0])
    travelTime = str(timedelta(hours=hr, minutes=min))
    
    price = re.findall("\$\d+\,?\d+", rawTicket)
    if len(price) == 0:
        price = None
    else:
        priceArr = price[0][1:].split(",")
        price = "".join(priceArr)

    flightNumber = re.findall("([A-Z0-9]{2} \d{2,4})\n", rawTicket)
    if (len(flightNumber) == 0):
        return None
    flightNumber = flightNumber[0]

    airlineCode = flightNumber.split(" ")[0]

    airportStr = re.findall("[A|P]M.+\([A-Z]{3}\)",rawTicket)
    departAirportStrArr = airportStr[0].split(" ")
    departAirportCode = departAirportStrArr.pop()
    departAirportCode = re.sub('[()]', '', departAirportCode)
    departAirportStr =  " ".join(departAirportStrArr)
    departAirportName = re.sub("[A|P]M(\+\d+)?", "", departAirportStr)

    arrivalAirportStrArr = airportStr[1].split(" ")
    arrivalAirportCode = arrivalAirportStrArr.pop()
    arrivalAirportCode = re.sub('[()]', '', arrivalAirportCode)
    arrivalAirportStr =  " ".join(arrivalAirportStrArr)
    arrivalAirportName = re.sub("[A|P]M(\+\d+)?", "", arrivalAirportStr)

    flightID = hashlib.sha256((flightNumber + departureDate + departureTime + arrivalDate + arrivalTime + departAirportCode + arrivalAirportCode).encode())
    flightID = flightID.hexdigest()

    ticketID = hashlib.sha256((flightID + ticketDate).encode())
    ticketID = ticketID.hexdigest()

    result = {}
    result["departAirport"] = (departAirportCode, departAirportName)
    result["arrivalAirport"] = (arrivalAirportCode, arrivalAirportName)
    result["flight"] = (flightID, flightNumber, airlineCode, departureDate, departureTime, arrivalDate, arrivalTime, travelTime, departAirportCode, arrivalAirportCode)
    result["ticket"] = (ticketID, flightID, ticketDate, "Economy", price)
    return result

# Making path, today's date
# if not os.path.isdir(dataPath):
#    os.makedirs(dataPath)

# dataPath = '../data/raw/' + date.today().strftime(("%Y.%m.%d"))

dataArray = []

for departCity in cities:
    for arrivalCity in cities:
        if departCity == arrivalCity:
            continue

        for timeDiff in range(1, daysAhead + 1):
            # determine the dates tickets should be crawled
            flightDate = today + timedelta(days=timeDiff)
            for flightClass in classOptions:
                # crawl by route, efficient
                queryUrl = ' from ' + departCity + ' to ' + arrivalCity + ' on ' + str(flightDate) + ' ' + ' '.join(flightProps) + ' ' + flightClass
                url = baseUrl + quote(queryUrl)
                # data is a list
                # should look like: [ticket information, ticket information,...]
                data = scrapeData(url)
                
                # WRITING DATA
                # outF = open(dataPath + "/flight_data.txt", "a", encoding="utf-8")        
                print('Writing data to a list')

                # write to a list
                for datum in data:
                    one_ticket = ''
                    one_ticket += "Ticket Date: " # could change to 'search data'
                    one_ticket += today.strftime("%m-%d-%Y\n")
                    one_ticket += "Departure Date: "
                    one_ticket += flightDate.strftime("%m-%d-%Y\n")
                    one_ticket += datum # Error is here, changed to utf-8
                    # outF.write("\n\nseperator\n\n")
                    dataArray.append(one_ticket)

                # outF.close()
                print('Stored data to list \'dataArray\'')

print(dataArray)

# inF = open(dataPath + "/flight_data.txt", encoding='utf-8')
# rawdata = inF.read()
# dataArray = rawdata.split("\n\nseperator\n\n")

flightTable = open(dataPath + '/flight.csv', 'w', newline='')
ticketTable = open(dataPath + '/ticket.csv', 'w', newline='')

flightWriter = csv.writer(flightTable)
ticketWriter = csv.writer(ticketTable)

flightFields = ["flight_id", "flight_number", "airline_code", "departure_date", "departure_time", "arrival_date", "arrival_time", "travel_time", "departure_airport", "arrival_airport"]
ticketFields = ["ticket_id", "flight_id", "purchase_date", "class", "price"]

# processRawTicket(dataArray[0])
flightWriter.writerow(flightFields)
ticketWriter.writerow(ticketFields)

for data in dataArray:
    # print("data",data)
    if (data == ""):
        continue
    processedData = processRawTicket(data)

    if not processedData:
        continue
    flightWriter.writerow(processedData["flight"])
    ticketWriter.writerow(processedData["ticket"])

flightTable.close()
ticketTable.close()
