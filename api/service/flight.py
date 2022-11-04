from flask import Blueprint, request, abort, jsonify
from datetime import timedelta, date
from service.db import db

flight_bp = Blueprint("flight", __name__)

# use cursor and select database
cursor = db.cursor()

def get_column_names():
    cursor.execute("select * from Flight limit 1")
    colNames = []
    for col in cursor.description:
        colNames.append(col[0])
    return colNames

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

    cursor.execute(sql_command)
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