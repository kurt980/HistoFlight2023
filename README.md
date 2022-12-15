# HistoFlight
Web application: https://histoflight.fly.dev/#/

(Database service on GoogleCloud is not turned on (due to charges))

## Intro to our Web App
[YouTube link](https://youtu.be/BMpqUacX58w)

## Interface Demo
### Flight Search
![image](./doc/images/interface1.png)
![image](./doc/images/interface3.png)
![image](./doc/images/interface4.png)
### Login
![image](./doc/images/interface2.png)
###  Comments
![image](./doc/images/interface5.png)

## How To Use (if you want to run locally） 
Download [Docker](https://www.docker.com/)

Go to dockerfile directory
```
docker build . -t histoflight
docker run -p 8080:8080 histoflight
```
Open http://localhost:8080/#/
## Contributors
We are team47 from CS411 Database System at UIUC

Yilun Fu (yilunf2@illinois.edu)

Weikun Wu (weikunw2@illinois.edu)

Henry Wang (henryw6@illinois.edu)

Chengyan Ji (cji10@illinois.edu)
