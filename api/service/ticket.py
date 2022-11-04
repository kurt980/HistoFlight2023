from flask import Blueprint, request, abort, jsonify
from datetime import timedelta, date
from service.db import db

ticket_bp = Blueprint("ticket", __name__)

# use cursor and select database
cursor = db.cursor()

def get_column_names():
    cursor.execute("select * from Ticket limit 1")
    colNames = []
    for col in cursor.description:
        colNames.append(col[0])
    return colNames

@ticket_bp.route("/tickets")
def get_tickets():
    colNames = get_column_names()

    queryCols = request.args.get("columns")
    print(queryCols)
    if (queryCols == None):
        queryCols = "*"
    else:
        for col in queryCols.split(","):
            if col not in colNames:
                return "Incorrect column names"
    
    sql_command = "select " + queryCols + " from Ticket limit 1000"

    cursor.execute(sql_command)
    l = list(cursor.fetchall())
    result = []
    for ticket in l:
        cur = {}
        for col in range(len(ticket)):
            if isinstance(ticket[col], timedelta):
                cur[cursor.description[col][0]] = str(ticket[col])
            elif isinstance(ticket[col], date):
                cur[cursor.description[col][0]] = ticket[col].strftime("%Y-%m-%d")
            else:
                cur[cursor.description[col][0]] = ticket[col]
        result.append(cur)
    return result