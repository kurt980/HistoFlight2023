from flask import Blueprint, request, abort, jsonify
from service.db import db

airport_bp = Blueprint("airport", __name__)

# use cursor and select database
cursor = db.cursor()

@airport_bp.route("/airports")
def get_airports():
    cursor.execute("select * from airport limit 1")
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
    
    sql_command = "select " + queryCols + " from airport"

    cursor.execute(sql_command)
    l = list(cursor.fetchall())
    result = []
    for airport in l:
        cur = {}
        for col in range(len(airport)):
            cur[cursor.description[col][0]] = airport[col]
        result.append(cur)
    return result