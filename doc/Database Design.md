-- create Airport table
CREATE TABLE Airport (
    IATA VARCHAR(10) PRIMARY KEY,
    airport_name VARCHAR(100) NOT NULL
);

-- create Airline table
CREATE TABLE Airline (
    IATA VARCHAR(10) PRIMARY KEY,
    airline_name VARCHAR(100) NOT NULL
);

-- create Comment table
CREATE TABLE Comment (
    comment_id INTEGER PRIMARY KEY,
    text TEXT NOT NULL,
    user_name VARCHAR(10) NOT NULL,
    airline VARCHAR(20) NOT NULL,
    FOREIGN KEY (user_name) REFERENCES User(user_name) ON DELETE CASCADE,
    FOREIGN KEY (airline) REFERENCES Airline(IATA) ON DELETE CASCADE
);

-- create User table
CREATE TABLE User (
    user_name VARCHAR(10) PRIMARY KEY,
    password VARCHAR(20) NOT NULL,
    email VARCHAR(30),
    first_name VARCHAR(50),
    last_name VARCHAR(50)
);

-- create Ticket table
CREATE TABLE Ticket (
    ticket_id VARCHAR(20) PRIMARY KEY,
    flight_id VARCHAR(20) NOT NULL,
    purchase_date DATE NOT NULL,
    CLASS VARCHAR(20),
    PRICE REAL NOT NULL,
    FOREIGN KEY (flight_id) REFERENCES Flight(flight_id) ON DELETE CASCADE
);

-- create Flight table
CREATE TABLE Flight (
    flight_id VARCHAR(20) PRIMARY KEY,
    flight_number VARCHAR(30) NOT NULL,
    airline_code VARCHAR(10) NOT NULL,
    departure_date DATE NOT NULL,
    departure_time TIME NOT NULL,
    arrival_date DATE NOT NULL,
    arrival_time TIME NOT NULL,
    travel_time TIME NOT NULL,
    departure_airport VARCHAR(10),
    arrival_airport VARCHAR(10),
    FOREIGN KEY (airline_code) REFERENCES Airline(IATA) ON DELETE CASCADE,
    FOREIGN KEY (departure_airport) REFERENCES Airport(IATA) ON DELETE CASCADE,
    FOREIGN KEY (arrival_airport) REFERENCES Airport(IATA) ON DELETE CASCADE
);

-- create Operate table
CREATE TABLE Operate (
    airline_IATA VARCHAR(10),
    airport_IATA VARCHAR(10),
    PRIMARY KEY (airline_IATA, airport_IATA)
    FOREIGN KEY (airline_IATA) REFERENCES Airline(IATA)
    FOREIGN KEY (airport_IATA) REFERENCES Airport(IATA)
);




## Advanced Query 1:
# get number of flights to an airport given a range of date
-- compute number of flights to a certain airport name given a range of date; provides accessibility for user
SELECT COUNT(Flight.flight_number) AS Visits, Airport.airport_name AS Airport

FROM Flight JOIN Airport ON Flight.arrival_airport = Airport.IATA

WHERE Flight.arrival_date BETWEEN '2022-09-20' AND '2020-10-20'

GROUP BY Airport.IATA

ORDER BY Visits ASC;

