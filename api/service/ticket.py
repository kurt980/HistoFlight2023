from flask import Blueprint, request, abort, jsonify
from datetime import timedelta, date
from service.db import DB

ticket_bp = Blueprint("ticket", __name__)

db = DB()

@ticket_bp.route("/tickets")
def get_tickets():
    return db.search('Ticket', {'limit': 1000})

@ticket_bp.route("/ticket")
def search_tickets():
    colNames = db.getColumnNames("Ticket")
    for column in request.args.keys():
        if column not in colNames and column != "limit":
            return "Incorrect column names"
    try:
        return db.search("Ticket", request.args.copy())
    except:
        return "Incorrect input"