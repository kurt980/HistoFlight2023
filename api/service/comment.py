from flask import Blueprint, request, abort, jsonify
from service.db import DB
from utils import sha256
from datetime import datetime

db = DB()

comment_bp = Blueprint("comment", __name__)


# get all comments
@comment_bp.route("/comments")
def get_comments():

    return db.search('Comment')

# search for certain comments
@comment_bp.route("/comment")
def search_comment():

    colNames = db.getColumnNames("Comment")
    for column in request.args.keys():
        if column not in colNames:
            return "Incorrect column names"

    try:
        return db.search('Comment', request.args.copy())
    except:
        return "Incorrect input"
  
# add a comment
@comment_bp.route("/comment", methods=['POST'])
def add_comments():

    colNames = db.getColumnNames("Comment")

    try:
        body = request.json.copy()
    except:
        body = request.form.copy()
    
    for colName in colNames:
        if body.get(colName) is None and colName != "comment_id":
            return "Missing " + colName

    if "comment_id" not in body.keys():
        s = ""
        for value in body.values():
            s += value
        body["comment_id"] = sha256(s + str(datetime.now()))
    
    return db.insert("Comment", body)

# delete comment
@comment_bp.route("/comment/<comment_id>", methods=['DELETE'])
def delete_comments(comment_id):

    db.delete("Comment", {"comment_id": comment_id})

    return "Comment id " + comment_id + " deleted"

# update comment
@comment_bp.route("/comment/<comment_id>", methods=['PUT'])
def update_comments(comment_id):
    try:
        body = request.json.copy()
    except:
        body = request.form.copy()
    
    return db.update("Comment", {"comment_id": comment_id}, body)
