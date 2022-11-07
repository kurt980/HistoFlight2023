from flask import Blueprint, request, abort, jsonify
from service.db import DB

airport_bp = Blueprint("airport", __name__)

db = DB()

@airport_bp.route("/airports")
def get_airports():

    colNames = db.get_column_names("Airport")

    queryCols = request.args.get("columns")
    print(queryCols)
    if (queryCols == None):
        queryCols = "*"
    else:
        for col in queryCols.split(","):
            if col not in colNames:
                return "Incorrect column names"

    return db.query("Airport")