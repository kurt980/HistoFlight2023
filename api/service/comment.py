from flask import Blueprint, request, abort, jsonify
from service.db import DB
from utils import sha256
from datetime import datetime
from service.auth import token_required

db = DB()

comment_bp = Blueprint("comment", __name__)


def getComment(commentID):
    return db.search('Comment', {'comment_id': commentID})

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
@token_required
def add_comments(current_user):

    colNames = db.getColumnNames("Comment")

    try:
        body = request.json.copy()
    except:
        body = request.form.copy()

    body['user_name'] = current_user['user_name']
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
@token_required
def delete_comments(current_user, comment_id):
    comment = getComment(comment_id)[0]
    if not comment:
        return "No comment with comment id " + comment_id + " found"
    if comment['user_name'] != current_user['user_name']:
        return "Not authorized to delete this comment"
    
    db.delete("Comment", {"comment_id": comment_id})

    return "Comment id " + comment_id + " deleted"

# update comment
@comment_bp.route("/comment/<comment_id>", methods=['PUT'])
@token_required
def update_comments(current_user, comment_id):
    comment = getComment(comment_id)[0]
    if not comment:
        return "No comment with comment id " + comment_id + " found"
    if comment['user_name'] != current_user['user_name']:
        return "Not authorized to update this comment"

    try:
        body = request.json.copy()
    except:
        body = request.form.copy()

    return db.update("Comment", {"comment_id": comment_id}, body)
