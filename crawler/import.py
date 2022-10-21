import csv
import re
from datetime import date, datetime
from datetime import timedelta
import hashlib

def processRawTicket(rawTicket):
    ticketDates = re.findall("Ticket Date: \d{1,2}-\d{1,2}-\d{4}", rawTicket)
    rawticketDate = ticketDates[0].split(" ")[-1]
    ticketDateObject = datetime.strptime(rawticketDate, "%m-%d-%Y")
    ticketDate = ticketDateObject.strftime("%m-%d-%Y")

    departureDates = re.findall("Departure Date: \d{1,2}-\d{1,2}-\d{4}", rawTicket)
    rawdepartureDate = departureDates[0].split(" ")[-1]

    flightTimes = re.findall("(\d{1,2}:\d{1,2} [A|P]M)(\+\d+)?", rawTicket)

    if (len(flightTimes) == 0):
        return None

    departureTimeStr = flightTimes[0][0]
    departureTimeObject = datetime.strptime(departureTimeStr, "%I:%M %p")
    departureTime = departureTimeObject.strftime("%H:%M")

    departureDateObject = datetime.strptime(rawdepartureDate, "%m-%d-%Y")
    arrivalDateObject = departureDateObject if flightTimes[1][1] == "" else departureDateObject + timedelta(days=int(flightTimes[1][1].split("+")[-1]))


    departureDate = departureDateObject.strftime("%m-%d-%Y")
    arrivalDate = arrivalDateObject.strftime("%m-%d-%Y")
    arrivalTimeStr = flightTimes[1][0]
    arrivalTimeObject = datetime.strptime(arrivalTimeStr, "%I:%M %p")
    arrivalTime = arrivalTimeObject.strftime("%H:%M")

    travelTime = re.findall("Travel time: ((\d{1,2} hr)? ?(\d{1,2} min)?)", rawTicket)

    # print("traveltime", travelTime)
    if len(travelTime) == 0:
        return None
    travelTime = travelTime[0][0]
    

    price = re.findall("\$\d+\,?\d+", rawTicket)
    if len(price) == 0:
        price = None
    else:
        priceArr = price[0][1:].split(",")
        price = "".join(priceArr)

    flightNumber = re.findall("[A-Z0-9]{2} \d{2,4}", rawTicket)
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

    flightID = hashlib.sha256((flightNumber + departureDate).encode())
    flightID = flightID.hexdigest()

    ticketID = hashlib.sha256((flightNumber + departureDate + ticketDate).encode())
    ticketID = ticketID.hexdigest()
    # print(flightID)
    # print(ticketID)

    result = {}
    result["departAirport"] = (departAirportCode, departAirportName)
    result["arrivalAirport"] = (arrivalAirportCode, arrivalAirportName)
    result["flight"] = (flightID, flightNumber, airlineCode, departureDate, departureTime, arrivalDate, arrivalTime, travelTime, departAirportCode, arrivalAirportCode)
    result["ticket"] = (ticketID, flightID, ticketDate, "Economy", price)
    return result

inF = open("flight_data.txt")
rawdata = inF.read()
dataArray = rawdata.split("\n\nseperator\n\n")

# print(processRawTicket(dataArray[0]))

flightTable = open('../data/flight.csv', 'a')
airportTable = open('../data/airport.csv', 'a')
ticketTable = open('../data/ticket.csv', 'a')

flightWriter = csv.writer(flightTable)
airportWriter = csv.writer(airportTable)
ticketWriter = csv.writer(ticketTable)

flightFields = ["flight_id", "flight_number", "airline_code", "departure_date", "departure_time", "arrival_date", "arrival_time", "travel_time", "departure_airport", "arrival_airport"]
airportFields = ["IATA", "airport_name"]
ticketFields = ["ticket_id", "flight_id", "purchase_date", "class", "price"]

flightWriter.writerow(flightFields)
airportWriter.writerow(airportFields)
ticketWriter.writerow(ticketFields)

# processedData = processRawTicket(dataArray[0])

airportSet= set()
flightSet = set()
for data in dataArray:
    # print("data",data)
    if (data == ""):
        continue
    processedData = processRawTicket(data)
    if processedData is None:
        continue
    if processedData["flight"][0] not in airportSet:
        flightWriter.writerow(processedData["flight"])
        flightSet.add(processedData["flight"][0])
    if processedData["departAirport"][0] not in airportSet:
        airportWriter.writerow(processedData["departAirport"])
        airportSet.add(processedData["departAirport"][0])
    if processedData["arrivalAirport"][0] not in airportSet:
        airportWriter.writerow(processedData["arrivalAirport"])
        airportSet.add(processedData["arrivalAirport"][0])
    ticketWriter.writerow(processedData["ticket"])
