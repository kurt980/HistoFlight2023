from flask import Blueprint, request, abort, jsonify
from service.db import DB

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
        return db.search('Comment', request.args)
    except:
        return "Incorrect input"
  
# add a comment
@comment_bp.route("/comment", methods=['POST'])
def add_comments():

    colNames = db.getColumnNames("Comment")

    for colName in colNames:
        if request.form.get(colName) is None and colName != "comment_id":
            return "Missing " + colName

    body = request.form.copy()

    # print(request.form)
    return db.insert("Comment", body)

# delete comment
@comment_bp.route("/delete", methods=['DELETE'])
def delete_comments(comment_id):

    db.delete("Comment", {"comment_id": comment_id})

    return "Comment id" + comment_id + "deleted"