DELIMITER //

CREATE PROCEDURE getFlightsCheaperThanAvg(
						IN departureAirport VARCHAR(10),
                        IN arrivalAirport VARCHAR(10),
                        IN departureDate DATE
                        )

    BEGIN
		
        -- declare variables
        DECLARE varAVG REAL;
		DECLARE latestDate DATE;
        
        DECLARE flightId VARCHAR(64);
        DECLARE flightNumber VARCHAR(30);
        DECLARE airlineCode VARCHAR(10);
        DECLARE departureTime TIME;
        DECLARE arrivalDate DATE;
        DECLARE arrivalTime TIME;
        DECLARE travelTime TIME;
        DECLARE varPrice REAL;
        DECLARE isCheap BOOL;
        
        -- declare cursor
        DECLARE exit_loop BOOLEAN DEFAULT FALSE;
        
        DECLARE custCur CURSOR FOR (SELECT flight_id, flight_number, airline_code, departure_time, arrival_date, arrival_time, travel_time, price
									FROM Ticket JOIN Flight USING(flight_id), (
										SELECT MAX(purchase_date) as date
										FROM Ticket
										) as t
									WHERE departure_date = departureDate
									AND purchase_date = t.date
									AND departure_airport = departureAirport
									AND arrival_airport = arrivalAirport
                                    );
                                
        DECLARE CONTINUE HANDLER FOR NOT FOUND SET exit_loop = TRUE;
		
        -- assign latestDate: latest date in Ticket
		SELECT * INTO latestDate FROM 
				(SELECT MAX(purchase_date) as date FROM Ticket) AS t;
        
        -- assign varAvg: fetch average price for recent 5 days
		SELECT avg INTO varAvg FROM 
				(
                SELECT AVG(price) AS avg  
				FROM Ticket JOIN Flight USING(flight_id)
				WHERE purchase_date = latestDate
				AND departure_date BETWEEN (departureDate - INTERVAL 2 DAY) AND (departureDate + INTERVAL 2 DAY)
				AND departure_airport = departureAirport
				AND arrival_airport = arrivalAirport
				GROUP BY departure_airport, arrival_airport
                ) as t1;
        
        # create new temporary table
		DROP TABLE IF EXISTS NewTable;
		CREATE TABLE NewTable (
			flight_id VARCHAR(64) PRIMARY KEY,
			flight_number VARCHAR(30) NOT NULL,
			airline_code VARCHAR(10) NOT NULL,
			departure_date DATE,
			departure_time TIME,
			arrival_date DATE,
			arrival_time TIME,
			travel_time TIME,
			departure_airport VARCHAR(10),
			arrival_airport VARCHAR(10),
            price REAL,
            avg_price REAL,
            is_cheap BOOL
		);
        
		OPEN custCur;
        cloop: LOOP
            FETCH custCur INTO flightId, flightNumber, airlineCode, departureTime, arrivalDate, arrivalTime, travelTime, varPrice;
            IF(exit_loop) THEN
                LEAVE cloop;
            END IF;
            
            IF(varPrice >= varAVG) THEN
                SET isCheap = FALSE;
            ELSE
                SET isCheap = TRUE;
            END IF;
            
            INSERT INTO NewTable VALUES (flightId, flightNumber, airlineCode, departureDate, departureTime, arrivalDate, arrivalTime, travelTime, departureAirport, arrivalAirport, varPrice, varAVG, isCheap);
            
        END LOOP cloop;
        CLOSE custCur;
        
        SELECT *
        FROM NewTable;
       
END//
    
DELIMITER ;


