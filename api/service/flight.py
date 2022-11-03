from flask import Blueprint, request, abort, jsonify
from service.db import db

flight_bp = Blueprint("flight", __name__)

# use cursor and select database
cursor = db.cursor()

@flight_bp.route("/flights")
def get_flights():
    cursor.execute("select * from flight limit 1")
    colNames = []
    for col in cursor.description:
        colNames.append(col[0])
    print(colNames)

    queryCols = request.args.get("columns")
    print(queryCols)
    if (queryCols == None):
        queryCols = "*"
    else:
        for col in queryCols.split(","):
            if col not in colNames:
                return "Incorrect column names"
    
    sql_command = "select " + queryCols + " from flight limit 1000"

    cursor.execute(sql_command)
    l = list(cursor.fetchall())
    result = []
    for airport in l:
        cur = {}
        for col in range(len(airport)):
            cur[cursor.description[col][0]] = airport[col]
        result.append(cur)
    return result