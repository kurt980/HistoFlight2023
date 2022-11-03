## Environment Setup
Run the following command to install python virtual environment
```sh
pip install virtualenv
```

Run the following command to create a python virtual environment
```sh
virtualenv flaskvenv
```

Run the following command to activate python virtual environment and install all dependencies
```sh
source flaskvenv/bin/activate
pip install -r requirements.txt
```

To deactivate from virtual environment, simply run
```sh
deactivate
```

## Config Change
go to `service/db.py`

and put in the correct address and credentials for the database

```python
db = Connection(
    host = 'localhost',
    user = 'root',
    password = 'cs411047',
)
```
## Run Server
Run the command
```sh
flask run
```

## Accessing API
After the server is running, open the following URLs in your browser

[airport](http://127.0.0.1:5000/api/airports)

[flights](http://127.0.0.1:5000/api/flights)
