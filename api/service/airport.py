from flask import Blueprint, request, abort, jsonify
from service.db import DB

airport_bp = Blueprint("airport", __name__)

db = DB()

@airport_bp.route("/airports")
def get_airports():
    return db.search("Airport")
