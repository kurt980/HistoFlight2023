from flask import Blueprint, request, abort, jsonify
from datetime import timedelta, date, datetime
from service.db import db
import hashlib

flight_bp = Blueprint("flight", __name__)

# use cursor and select database
cursor = db.cursor()

def get_column_names():
    cursor.execute("select * from Flight limit 1")
    colNames = []
    for col in cursor.description:
        colNames.append(col[0])
    return colNames

# execute the sql query and return a list of parsed data
def query(sql):
    print("Calling MySQL")
    print(sql)
    cursor.execute(sql)
    l = list(cursor.fetchall())
    result = []
    for flight in l:
        cur = {}
        for col in range(len(flight)):
            if isinstance(flight[col], timedelta):
                cur[cursor.description[col][0]] = str(flight[col])
            elif isinstance(flight[col], date):
                cur[cursor.description[col][0]] = flight[col].strftime("%Y-%m-%d")
            else:
                cur[cursor.description[col][0]] = flight[col]
        result.append(cur)
    return result

# Get the first 1000 flights in the database
# Example usage:
# GET http://127.0.0.1:5000/api/flights
@flight_bp.route("/flights")
def get_flights():
    colNames = get_column_names()

    queryCols = request.args.get("columns")
    print(queryCols)
    if (queryCols == None):
        queryCols = "*"
    else:
        for col in queryCols.split(","):
            if col not in colNames:
                return "Incorrect column names"
    
    sql_command = "select " + queryCols + " from Flight limit 1000"

    return query(sql_command)

# Example usage:
# GET http://127.0.0.1:5000/api/flight?departure_airport=‘LAX‘&arrival_airport=‘ORD‘&airline_code='AA'
@flight_bp.route("/flight")
def search_flight():
    colNames = get_column_names()
    for column in request.args.keys():
        if column not in colNames:
            return "Incorrect column names"

    args = "where"
    for column in request.args.keys():
        args = args + " " + column + " = " + request.args.get(column) + " AND"
    
    if args.endswith(" AND"):
        args = args[0:- 4]
    sql_command = "select * from Flight " + args

    try:
        return query(sql_command)
    except:
        return "Incorrect input"


def get_new_id():
    return '1'

@flight_bp.route("/flight", methods=['POST'])
def add_flight():
    colNames = get_column_names()

    for colName in colNames:
        if request.form.get(colName) is None and colName != "flight_id":
            return "Missing " + colName
    body = request.form.copy()
    
    body["departure_date"] = datetime.strptime(body["departure_date"], "%Y-%m-%d").strftime("%Y-%m-%d")
    body["arrival_date"] = datetime.strptime(body["arrival_date"], "%Y-%m-%d").strftime("%Y-%m-%d")
    body["departure_time"] = datetime.strptime(body["departure_time"], "%I:%M").strftime("%H:%M")
    body["arrival_time"] = datetime.strptime(body["arrival_time"], "%I:%M").strftime("%H:%M")
    body["flight_id"] = hashlib.sha256((body["flight_number"] + body["departure_date"] + body["departure_time"] + body["arrival_date"] + body["arrival_time"] + body["departure_airport"] + body["arrival_airport"]).encode()).hexdigest()

    values = []
    for colName in colNames:
        values.append(body[colName])

    
    sql_command = "insert into Flight values('" + "','".join(values) + "')"
    print("Inserting into MySQL")
    print(sql_command)
    cursor.execute(sql_command)
    db.commit()
    return request.form

@flight_bp.route("/flight/<flight_id>", methods=['DELETE'])
def remove_flight(flight_id):
    sql_command = "delete from Flight where flight_id = '" + flight_id + "'"
    print("Deleting from MySQL")
    print(sql_command)
    cursor.execute(sql_command)
    db.commit()
    return "Deleted"