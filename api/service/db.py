from pymysql import Connection

db = Connection(
    host = 'localhost',
    user = 'root',
    password = 'cs411047',
)

db.select_db("project")
