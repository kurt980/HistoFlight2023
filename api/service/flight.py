from flask import Blueprint, request
from datetime import timedelta, date, datetime
from service.db import DB
import hashlib

flight_bp = Blueprint("flight", __name__)

db = DB()

# Get the first 1000 flights in the database
# Example usage:
# GET http://127.0.0.1:5000/api/flights
@flight_bp.route("/flights")
def get_flights():
    colNames = db.get_column_names("Flight")

    queryCols = request.args.get("columns")
    print(queryCols)
    if (queryCols == None):
        queryCols = "*"
    else:
        for col in queryCols.split(","):
            if col not in colNames:
                return "Incorrect column names"

    return db.search("Flight", {'limit': 1000})

# Example usage:
# GET http://127.0.0.1:5000/api/flight?departure_airport=‘LAX‘&arrival_airport=‘ORD‘&airline_code='AA'
@flight_bp.route("/flight")
def search_flight():
    colNames = db.get_column_names("Flight")
    for column in request.args.keys():
        if column not in colNames:
            return "Incorrect column names from flask"
    try:
        return db.search("Flight", request.args)
    except:
        return "Incorrect input"

def get_flight_by_ID(id):
    try:
        return db.search("Flight", {'flight_id': id})
    except:
        return "Incorrect input"

@flight_bp.route("/flight", methods=['POST'])
def add_flight():
    colNames = db.get_column_names("Flight")

    for colName in colNames:
        if request.form.get(colName) is None and colName != "flight_id":
            return "Missing " + colName
    
    body = request.form.copy()
    try:
        body["departure_date"] = datetime.strptime(body["departure_date"], "%Y-%m-%d").strftime("%Y-%m-%d")
        body["arrival_date"] = datetime.strptime(body["arrival_date"], "%Y-%m-%d").strftime("%Y-%m-%d")
        body["departure_time"] = datetime.strptime(body["departure_time"], "%I:%M").strftime("%H:%M")
        body["arrival_time"] = datetime.strptime(body["arrival_time"], "%I:%M").strftime("%H:%M")
        body["travel_time"] = str(datetime.strptime(body["arrival_time"], "%I:%M") - datetime.strptime(body["departure_time"], "%I:%M"))
        body["flight_id"] = hashlib.sha256((body["flight_number"] + body["departure_date"] + body["departure_time"] + body["arrival_date"] + body["arrival_time"] + body["departure_airport"] + body["arrival_airport"]).encode()).hexdigest()
    except:
        return "Incorrect date or time format, please use YYYY-MM-DD and HH:MM"

    return db.insert("Flight", body)

@flight_bp.route("/flight/<flight_id>", methods=['DELETE'])
def remove_flight(flight_id):
    db.delete("Flight", {"flight_id": flight_id})

    return "Deleted"