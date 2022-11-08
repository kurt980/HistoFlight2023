from pymysql import connect
from datetime import timedelta, date, datetime
import config

class DB:
    # Connect to DB using config file
    def connectToDB(self):
        db = connect(**config.DB_CONFIG)
        db.select_db("project")
        return db

    # Get all the columns of a table
    def getColumnNames(self, table):
        sqlCommand = "SELECT * FROM " + table + " LIMIT 1"
        return self.execute(sqlCommand)[0].keys()

    # Execute the sql command and return any results if there is any
    def execute(self, sql):
        print(sql)
        db = self.connectToDB()
        cursor = db.cursor()
        cursor.execute(sql)
        l = list(cursor.fetchall())
        result = []
        for row in l:
            cur = {}
            for col in range(len(row)):
                if isinstance(row[col], timedelta):
                    cur[cursor.description[col][0]] = str(row[col])
                elif isinstance(row[col], date):
                    cur[cursor.description[col][0]] = row[col].strftime("%Y-%m-%d")
                else:
                    cur[cursor.description[col][0]] = row[col]
            result.append(cur)
        db.commit()
        db.close()
        return result
    
    # Search the database from a table and return all results
    # search("Flight", {flight_number, "AA 2330"})
    # If no paramSet is specified, return all rows
    def search(self, table, paramSet={}):
        colNames = self.getColumnNames(table)

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
        
        sqlCommand = "SELECT * FROM " + table + queryArgs + limitArgs
        result = self.execute(sqlCommand)

        return result

    # Insert a value into a table in the database and return the inserted row
    # insert("Flight", {flight_number, "AA 2330"})
    def insert(self, table, paramSet):
        colNames = self.getColumnNames(table)

        for colName in colNames:
            if paramSet[colName] is None:
                return "Missing " + colName

        values = []
        for colName in colNames:
            values.append(paramSet[colName])

        
        sqlCommand = "INSERT INTO " + table + " VALUES('" + "','".join(values) + "')"
        try:
            print("Inserting into MySQL")
            self.execute(sqlCommand)
            return self.search(table, paramSet)
        except:
            return []

    # Delete a value of a table from the database
    # and return whether the operation was successful
    # delete("Flight", {flight_number, "AA 2330"})
    def delete(self, table, paramSet):

        args = "WHERE"
        for column, value in paramSet.items():
            args = args + " " + column + " = '" + value + "' AND"
        
        if args.endswith(" AND"):
            args = args[0:- 4]

        sqlCommand = "DELETE FROM " + table + " " + args
        try:
            print("Deleting from MySQL")
            self.execute(sqlCommand)
            return True
        except:
            return False

    def getTicketsCheaperThanAvg(self, departureAirport, arrivalAirport, departureDate):
        departureDateObject = datetime.strptime(departureDate, "%Y-%m-%d")
        fromDate = (departureDateObject - timedelta(days=4)).strftime("%Y-%m-%d")
        sqlCommand = """
            SELECT *
            FROM Ticket JOIN Flight USING(flight_id)
            WHERE departure_date = '{}'
            AND departure_airport = '{}'
            AND arrival_airport = '{}'
            AND price <=
                (SELECT AVG(price)    
                FROM Ticket JOIN Flight USING(flight_id)
                WHERE departure_date BETWEEN '{}' AND '{}'
                AND departure_airport = '{}'
                AND arrival_airport = '{}'
                GROUP BY departure_airport, arrival_airport)
        """.format(departureDate, departureAirport, arrivalAirport, fromDate, departureDate, departureAirport, arrivalAirport)

        return self.execute(sqlCommand)