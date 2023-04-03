import csv
import hashlib
import re
from datetime import date, datetime, timedelta
from pathlib import Path

import pandas as pd


def processRawTicket(rawTicket):
    ticketDates = re.findall("Ticket Date: \d{1,2}-\d{1,2}-\d{4}", rawTicket)
    rawticketDate = ticketDates[0].split(" ")[-1]
    ticketDateObject = datetime.strptime(rawticketDate, "%m-%d-%Y")
    ticketDate = ticketDateObject.strftime("%Y-%m-%d")

    departureDates = re.findall("Departure Date: \d{1,2}-\d{1,2}-\d{4}", rawTicket)
    rawdepartureDate = departureDates[0].split(" ")[-1]

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

# dataPath = '../data/raw/' + date.today().strftime(("%Y.%m.%d"))
# my_date = date(2023, 3, 30)
# dataPath = '../HistoFlight2023/data/raw/' + my_date.strftime(("%Y.%m.%d"))
today = date.today()
dataPath = '../HistoFlight2023/data/raw/' + today.strftime(("%Y.%m.%d"))

inF = open(dataPath + "/flight_data.txt", encoding='utf-8')
rawdata = inF.read()
dataArray = rawdata.split("\n\nseperator\n\n")

flightTable = open(dataPath + '/flight.csv', 'w')
ticketTable = open(dataPath + '/ticket.csv', 'w')

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

# reads from the written files and check for duplicates
# THIS NEEDS TO BE FIXED
# flights = pd.read_csv(dataPath + "/flight.csv")
# flights_no_dup = flights.drop_duplicates()
# if (flights.flight_id.count() != flights_no_dup.flight_id.count()):
#     print("Duplicate flight detected")
#     Path(dataPath + "/flight.csv").unlink(missing_ok=True)

# tickets = pd.read_csv(dataPath + "/ticket.csv")
# tickets_no_dup = tickets.drop_duplicates()
# if (tickets.ticket_id.count() != tickets_no_dup.ticket_id.count()):
#     print("Duplicate ticket detected")
#     Path(dataPath + "/ticket.csv").unlink(missing_ok=True)
