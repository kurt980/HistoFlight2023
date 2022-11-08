from pymysql import connect
from datetime import timedelta, date, datetime
import config

class DB:
    # Connect to DB using config file
    def connect_to_db(self):
        db = connect(**config.DB_CONFIG)
        db.select_db("project")
        return db

    # Get all the columns of a table
    def get_column_names(self, table):
        sqlCommand = "SELECT * FROM " + table + " LIMIT 1"
        return self.execute(sqlCommand)[0].keys()

    # Execute the sql command and return any results if there is any
    def execute(self, sql):
        print(sql)
        db = self.connect_to_db()
        cursor = db.cursor()
        cursor.execute(sql)
        l = list(cursor.fetchall())
        result = []
        for flight in l:
            cur = {}
            for col in range(len(flight)):
                if isinstance(flight[col], timedelta):
                    cur[cursor.description[col][0]] = str(flight[col])
                elif isinstance(flight[col], date):
                    cur[cursor.description[col][0]] = flight[col].strftime("%Y-%m-%d")
                else:
                    cur[cursor.description[col][0]] = flight[col]
            result.append(cur)
        return result
    
    # Search the database from a table and return all results
    # search("Flight", {flight_number, "AA 2330"})
    # If no paramSet is specified, return all rows
    def search(self, table, paramSet={}):
        colNames = self.get_column_names(table)

        db = self.connect_to_db()
        try:
            limitArgs = " LIMIT " + str(paramSet.pop('limit'))
        except:
            limitArgs = ""

        for column in paramSet:
            if column not in colNames:
                return "Incorrect column names"
        
        if len(paramSet) == 0:
            queryArgs = ''
        else:
            queryArgs = " WHERE"
            for column, value in paramSet.items():
                if column.lower() == "limit":
                    limit = value
                    continue
                queryArgs = queryArgs + " " + column + " = '" + value + "' AND"
            
            if queryArgs.endswith(" AND"):
                queryArgs = queryArgs[0:- 4]
        
        sql_command = "SELECT * FROM " + table + queryArgs + limitArgs
        result = self.execute(sql_command)
        db.close()
        return result

    # Insert a value into a table in the database and return the inserted row
    # insert("Flight", {flight_number, "AA 2330"})
    def insert(self, table, paramSet):
        colNames = self.get_column_names(table)

        db = self.connect_to_db()
        cursor = db.cursor()
        for colName in colNames:
            if paramSet[colName] is None:
                return "Missing " + colName

        values = []
        for colName in colNames:
            values.append(paramSet[colName])

        
        sql_command = "INSERT INTO " + table + " VALUES('" + "','".join(values) + "')"
        try:
            print("Inserting into MySQL")
            print(sql_command)
            cursor.execute(sql_command)
            db.commit()
            db.close()
            return self.search(table, paramSet)
        except:
            return []

    # Delete a value of a table from the database
    # and return whether the operation was successful
    # delete("Flight", {flight_number, "AA 2330"})
    def delete(self, table, paramSet):
        db = self.connect_to_db()
        cursor = db.cursor()

        args = "WHERE"
        for column, value in paramSet.items():
            args = args + " " + column + " = '" + value + "' AND"
        
        if args.endswith(" AND"):
            args = args[0:- 4]

        sql_command = "DELETE FROM " + table + " " + args
        print("Deleting from MySQL")
        print(sql_command)
        try:
            cursor.execute(sql_command)
            db.commit()
            return True
        except:
            return False