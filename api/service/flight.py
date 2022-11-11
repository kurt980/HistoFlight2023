from flask import Blueprint, request
from datetime import timedelta, date, datetime
from service.db import DB
from utils import sha256

flight_bp = Blueprint("flight", __name__)

db = DB()

# Get the first 1000 flights in the database
# Example usage:
# GET http://127.0.0.1:5000/api/flights
@flight_bp.route("/flights")
def get_flights():
    return db.search("Flight", {'limit': 1000})

# Example usage:
# GET http://127.0.0.1:5000/api/flight?departure_airport=LAX&arrival_airport=ORD&airline_code=AA
@flight_bp.route("/flight")
def search_flight():
    colNames = db.getColumnNames("Flight")
    for column in request.args.keys():
        if column not in colNames and column != "limit":
            return "Incorrect column names"
    try:
        return db.search("Flight", request.args.copy())
    except:
        return "Incorrect input"

@flight_bp.route("/flight", methods=['POST'])
def add_flight():
    colNames = db.getColumnNames("Flight")
    try:
        body = request.json.copy()
    except:
        body = request.form.copy()
    
    for colName in colNames:
        if body.get(colName) is None and colName != "flight_id":
            return "Missing " + colName
    
    try:
        body["departure_date"] = datetime.strptime(body["departure_date"], "%Y-%m-%d").strftime("%Y-%m-%d")
        body["arrival_date"] = datetime.strptime(body["arrival_date"], "%Y-%m-%d").strftime("%Y-%m-%d")
        body["departure_time"] = datetime.strptime(body["departure_time"], "%I:%M").strftime("%H:%M")
        body["arrival_time"] = datetime.strptime(body["arrival_time"], "%I:%M").strftime("%H:%M")
        body["travel_time"] = str(datetime.strptime(body["arrival_time"], "%I:%M") - datetime.strptime(body["departure_time"], "%I:%M"))
        body["flight_id"] = sha256(body["flight_number"] + body["departure_date"] + body["departure_time"] + body["arrival_date"] + body["arrival_time"] + body["departure_airport"] + body["arrival_airport"])
    except:
        return "Incorrect date or time format, please use YYYY-MM-DD and HH:MM"

    return db.insert("Flight", body)

@flight_bp.route("/flight/<flight_id>", methods=['PUT'])
def update_flight(flight_id):
    try:
        body = request.json.copy()
    except:
        body = request.form.copy()
    
    return db.update("Flight", {"flight_id": flight_id}, body)

@flight_bp.route("/flight/<flight_id>", methods=['GET'])
def get_flight_by_ID(flight_id):
    try:
        return db.search("Flight", {'flight_id': flight_id})
    except:
        return "Incorrect input"

def get_flight_by_IDs(ids):
    flights = []
    for id in ids:
        flights.extend(get_flight_by_ID(id))
    return flights

@flight_bp.route("/flight/<flight_id>", methods=['DELETE'])
def remove_flight(flight_id):
    db.delete("Flight", {"flight_id": flight_id})

    return "Deleted"

# /api/getFlightsCheaperThanAvg?departure_airport=SFO&arrival_airport=ORD&departure_date=2022-11-6
@flight_bp.route("/getFlightsCheaperThanAvg")
def get_flights_Cheaper_than_avg():
    colNames = db.getColumnNames("Flight")
    for column in request.args.keys():
        if column not in colNames:
            return "Incorrect column names"
    

    try:
        tickets = db.getTicketsCheaperThanAvg(request.args.get("departure_airport"), request.args.get("arrival_airport"), request.args.get("departure_date"))
        flightIDs = [x['flight_id'] for x in tickets]
        return get_flight_by_IDs(flightIDs)
    except:
        return "Incorrect input"

# /api/getFlightAvgPrice/000c5e71991b00f7476973473ea02d681632af69bdb5261d20917c4b8dc28ad8
@flight_bp.route("/getFlightAvgPrice/<flight_id>")
def get_flight_avg_price(flight_id):
    return db.getFlightAvgPrice(flight_id)