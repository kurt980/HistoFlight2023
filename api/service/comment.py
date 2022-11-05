from flask import Blueprint, request, abort, jsonify
from service.db import db

comment_bp = Blueprint("comment", __name__)

# use cursor and select database
cursor = db.cursor()

# def get_column_names():
#     cursor.execute("select * from Comment limit 1")
#     colNames = []
#     for col in cursor.description:
#         colNames.append(col[0])
#     return colNames

@comment_bp.route("/comments")
def get_comments():

    # colNames = get_column_names()

    queryAirline = request.args.get("airline")
    queryUser = request.args.get("user_name")

    print(request.args)

    where_clause = ""

    if (queryAirline != None and queryUser != None):
        where_clause = " where airline =" + queryAirline + " and user_name =" + queryUser
    elif (queryAirline == None and queryUser != None):
        where_clause = " where user_name =" + queryUser
    elif (queryAirline != None and queryUser == None):
        where_clause = " where airline =" + queryAirline
    else:
        sql_command = ""

    sql_command = "select * from Comment" + where_clause


    cursor.execute(sql_command)
    l = list(cursor.fetchall())
    result = []
    for comment in l:
        cur = {}
        for col in range(len(comment)):
            cur[cursor.description[col][0]] = comment[col]
        result.append(cur)
    return result