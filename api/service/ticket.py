from flask import Blueprint, request, abort, jsonify
from datetime import timedelta, date
from service.db import DB

ticket_bp = Blueprint("ticket", __name__)

db = DB()

@ticket_bp.route("/tickets")
def get_tickets():
    colNames = db.get_column_names("Ticket")

    queryCols = request.args.get("columns")
    print(queryCols)
    if (queryCols == None):
        queryCols = "*"
    else:
        for col in queryCols.split(","):
            if col not in colNames:
                return "Incorrect column names"

    return db.query('Ticket', {'limit': 1000})