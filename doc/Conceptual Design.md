## UML diagram

![image](./images/UML.png)

## Assumption

1. We think a user can write many comments and a comment is associated with exactly one user<br>
2. We think a comment is attached to exactly one airline and an airline can have many comments<br>
3. We think an airline can operate in at least one airports and an airport have at least one airline<br>
4. We think an airline offers at least one flights and each flight is associated with exactly one airline<br>
5. We think each flight issues at least one ticket and each ticket is associated with exactly one flight<br>
6. We think each flight departs from exactly one airport and each airport has at least one departure flight<br>
7. We think each flight arrives from exactly one airport and each airport has at least one arrival flight<br>



## Relational Schema

**Ticket**( <br>
&emsp;&emsp;  ticket_id:    &emsp;&emsp;&emsp;&emsp;     varchar(64) &emsp;[PK]<br>
&emsp;&emsp;  flight_id:    &emsp;&emsp;&emsp;&emsp;     varchar(64) &emsp;&nbsp;[FK to Flight.flight_id]<br>
&emsp;&emsp;  purchase_date: &emsp;     date  <br>
&emsp;&emsp;  class: &emsp;&emsp;&emsp;&emsp;&emsp;&ensp;     varchar(50)  <br>
&emsp;&emsp;  price: &emsp;&emsp;&emsp;&emsp;&emsp;&ensp;     real  <br>


**Flight**( <br>
&emsp;&emsp;  flight_id:    &emsp;&emsp;&emsp;&emsp;&nbsp;     varchar(64) &emsp;[PK]<br>
&emsp;&emsp;  flight_number:    &emsp;&ensp;&nbsp;     varchar(30)  <br>
&emsp;&emsp;  airline_code: &emsp;&nbsp;&emsp;&nbsp;     varchar(10) &emsp;&nbsp; [FK to Airline.IATA]<br>
&emsp;&emsp;  departure_date: &ensp;&nbsp;&nbsp;     date  <br>
&emsp;&emsp;  departure_time: &ensp;&nbsp;&nbsp;    time  <br>
&emsp;&emsp;  arrival_date: &emsp;&emsp;&ensp;&nbsp;     date  <br>
&emsp;&emsp;  arrival_time: &emsp;&emsp;&ensp;&nbsp;     time  <br>
&emsp;&emsp;  travel_time: &emsp;&emsp;&ensp;&nbsp;&nbsp;     time <br>
&emsp;&emsp;  departure_airport: &nbsp;     varchar(10)&emsp;&nbsp;[FK to Airport.IATA]<br>
&emsp;&emsp;  arrival_airport: &emsp;&ensp;&nbsp;     varchar(10) &emsp;[FK to Airport.IATA]<br>

**Airport**( <br>
&emsp;&emsp;  IATA:    &emsp;&emsp;&emsp;&emsp;&emsp;&ensp;&ensp;     varchar(10) &emsp;[PK]<br>
&emsp;&emsp;  airport_name:    &emsp;&emsp;     varchar(50) &emsp;

**User**( <br>
&emsp;&emsp;  user_name:    &emsp;&emsp;&emsp;&nbsp;     varchar(100) &emsp;[PK]<br>
&emsp;&emsp;  password:    &emsp;&emsp;&emsp;&ensp;&nbsp;     varchar(100) <br>
&emsp;&emsp;  email: &emsp;&ensp;&nbsp;&emsp;&emsp;&emsp;&nbsp;&ensp;     varchar(100)<br>
&emsp;&emsp;  firstname: &emsp;&ensp;&nbsp;&emsp;&ensp;&ensp;    varchar(50)<br>
&emsp;&emsp;  lastname: &emsp;&ensp;&nbsp;&emsp;&emsp;&nbsp;     varchar(50)<br>

**Comment**( <br>
&emsp;&emsp;  comment_id:    &emsp;&emsp;&ensp;     varchar(100) &emsp;[PK]<br>
&emsp;&emsp;  text:    &emsp;&emsp;&emsp;&emsp;&emsp;&ensp;&ensp;&nbsp;     varchar(100) <br>
&emsp;&emsp;  user_name:    &emsp;&emsp;&emsp;&nbsp;     varchar(100) &emsp;[FK to User.user_name]<br>
&emsp;&emsp;  airline: &emsp;&ensp;&nbsp;&emsp;&emsp;&emsp;&ensp;     varchar(100)&emsp;&nbsp;[FK to Airline.IATA]<br>

**Airline**( <br>
&emsp;&emsp;  IATA:    &emsp;&emsp;&emsp;&emsp;&emsp;&ensp;&ensp;    varchar(10) &emsp;[PK]<br>
&emsp;&emsp;  airline_name:    &emsp;&emsp;&ensp;     varchar(100) <br>

**Operate**( <br>
&emsp;&emsp;  airline_IATA:   &emsp;&emsp;&ensp;&ensp;    varchar(10) &emsp;[PK][FK to Airport.IATA]<br>
&emsp;&emsp;  airport_IATA:    &emsp;&emsp;&ensp;&nbsp;     varchar(10) &emsp;[PK][FK to Airline.IATA]<br>


















