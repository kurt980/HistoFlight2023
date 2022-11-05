from pymysql import Connection

db = Connection(
    host = '34.67.249.196',
    user = 'root',
    password = 'cs411047',
)

db.select_db("project")
