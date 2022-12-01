from flask import Blueprint, request, abort, jsonify
from datetime import timedelta, date
from service.db import DB

ticket_bp = Blueprint("ticket", __name__)

db = DB()

@ticket_bp.route("/tickets")
def get_tickets():
    return db.search('Ticket', {'limit': 1000})

@ticket_bp.route("/ticket/<flight_id>")
def get_tickets_by_flight_id(flight_id):
    return db.search('Ticket', {'flight_id': flight_id})
