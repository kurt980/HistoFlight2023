from flask import Blueprint, request, abort, jsonify
from service.db import DB

airline_bp = Blueprint("airline", __name__)

db = DB()

@airline_bp.route("/airlines")
def get_airports():
    return db.search("Airline")
