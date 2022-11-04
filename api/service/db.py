from pymysql import Connection

db = Connection(
    host = 'IPaddress',
    user = 'root',
    password = 'cs411047',
)

db.select_db("project")
