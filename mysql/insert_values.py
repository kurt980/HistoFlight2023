import pandas as pd
import numpy as np
from datetime import datetime, date, timedelta
from pymysql import Connection

conn = Connection(
    host = '34.67.249.196',
    user = 'root',
    password = 'cs411047',
)
# cursor
cursor = conn.cursor()
# use database
conn.select_db("project")

# import data
# today_date = date.today().strftime("%Y.%m.%d") 
# df_flight = pd.read_csv("E:\\UIUC\\CS411 Database Systems\\fa22-cs411-A-team047-Pepsi\\data\\%s\\flight.csv"%today_date,header=None)
# df_ticket = pd.read_csv("E:\\UIUC\\CS411 Database Systems\\fa22-cs411-A-team047-Pepsi\\data\\%s\\ticket.csv"%today_date,header=None)

df_flight = pd.read_csv("E:\\UIUC\\CS411 Database Systems\\fa22-cs411-A-team047-Pepsi\\data\\2022.12.02\\flight.csv",header=None)
df_ticket = pd.read_csv("E:\\UIUC\\CS411 Database Systems\\fa22-cs411-A-team047-Pepsi\\data\\2022.12.02\\ticket.csv",header=None)

# fill nan in 'price' in ticket
df_ticket[4] = df_ticket[4].fillna('NULL')

# insert values to Flight
def save_to_flight(df_flight):
    
    for i in range(1,len(df_flight)):
        try:
            sql = "insert into Flight(flight_id, flight_number, airline_code, departure_date, departure_time, arrival_date, arrival_time, travel_time, departure_airport, arrival_airport) \
            values('%s','%s','%s','%s','%s','%s','%s','%s','%s','%s'); " \
            %(df_flight.loc[i,0],df_flight.loc[i,1],df_flight.loc[i,2],df_flight.loc[i,3],df_flight.loc[i,4], \
                df_flight.loc[i,5],df_flight.loc[i,6],df_flight.loc[i,7],df_flight.loc[i,8],df_flight.loc[i,9])
            cursor.execute(sql)
            conn.commit()
            print(f"successfully inserted record {i} in Flight")
        except:
            continue

# define function to insert values to Tickect
def save_to_ticket(df_ticket):
    
    for i in range(1,len(df_ticket)):
        try:
            sql = "insert into Ticket(ticket_id, flight_id, purchase_date, class, price) values('%s','%s','%s','%s',%s); " \
            %(df_ticket.loc[i,0],df_ticket.loc[i,1],df_ticket.loc[i,2],df_ticket.loc[i,3],df_ticket.loc[i,4])
            cursor.execute(sql)
            conn.commit()
            print(f"successfully inserted record {i} in Ticket")
        except:
            continue



save_to_flight(df_flight)
save_to_ticket(df_ticket)

print("All missions completed")

# close connection
conn.close()