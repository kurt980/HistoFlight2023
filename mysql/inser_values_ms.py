import pandas as pd
import numpy as np
from datetime import datetime, date, timedelta
import pyodbc

# Connect to SQL Server
server = 'your_server_name'
database = 'your_database_name'
username = 'your_username'
password = 'your_password'
driver = '{ODBC Driver 17 for SQL Server}'
cnxn = pyodbc.connect(f'DRIVER={driver};SERVER={server};DATABASE={database};UID={username};PWD={password}')
cursor = cnxn.cursor()

# Read flight and ticket data
today_date = date.today().strftime("%Y.%m.%d") 
df_flight = pd.read_csv("../data/%s/flight.csv" % today_date, header=None)
df_ticket = pd.read_csv("../data/%s/ticket.csv" % today_date, header=None)

# Fill NaN values in 'price' column of ticket dataframe
df_ticket[4] = df_ticket[4].fillna('NULL')

# Define function to insert data into the Flight table
def save_to_flight(df_flight):
    for i in range(1, len(df_flight)):
        try:
            sql = f"INSERT INTO Flight(flight_id, flight_number, airline_code, departure_date, departure_time, arrival_date, arrival_time, travel_time, departure_airport, arrival_airport) \
                    VALUES ('{df_flight.loc[i,0]}', '{df_flight.loc[i,1]}', '{df_flight.loc[i,2]}', '{df_flight.loc[i,3]}', '{df_flight.loc[i,4]}', \
                    '{df_flight.loc[i,5]}', '{df_flight.loc[i,6]}', '{df_flight.loc[i,7]}', '{df_flight.loc[i,8]}', '{df_flight.loc[i,9]}'); "
            cursor.execute(sql)
            cnxn.commit()
            print(f"Successfully inserted record {i} into Flight table")
        except:
            continue

# Define function to insert data into the Ticket table
def save_to_ticket(df_ticket):
    for i in range(1, len(df_ticket)):
        try:
            sql = f"INSERT INTO Ticket(ticket_id, flight_id, purchase_date, class, price) \
                    VALUES ('{df_ticket.loc[i,0]}', '{df_ticket.loc[i,1]}', '{df_ticket.loc[i,2]}', '{df_ticket.loc[i,3]}', {df_ticket.loc[i,4]}); "
            cursor.execute(sql)
            cnxn.commit()
            print(f"Successfully inserted record {i} into Ticket table")
        except:
            continue

# Call functions to insert data into tables
save_to_flight(df_flight)
save_to_ticket(df_ticket)

# Close connection
cnxn.close()
