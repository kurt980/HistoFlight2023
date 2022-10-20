
-- creat Airport table
CREATE TABLE Airport (
    IATA VARCHAR(3) PRIMARY KEY
    airport_name VARCHAR(100) NOT NULL
)

-- create Airline table
CREATE TABLE Airline (
    IATA VARCHAR(2) PRIMARY KEY
    airline_name VARCHAR(100) NOT NULL
)

-- create Comment table
CREATE TABLE Comment (
    comment_id INTEGER PRIMARY KEY
    text TEXT NOT NULL
)

-- create User table
CREATE TABLE User (
    username VARCHAR(50) PRIMARY KEY
    password VARCHAR(50) NOT NULL
    email VARCHAR(50)
    first_name VARCHAR(50)
    last_name VARCHAR(50)
)

-- create Ticket table
CREATE TABLE Ticket (
    
)
