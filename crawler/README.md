# Google Flight Crawler
This is a web crawler that crawl flight data from Google Flight

## Environment Setup
Run the following command to install python virtual environment
```sh
pip install virtualenv
```

Run the following command to create a python virtual environment
```sh
virtualenv venv
```

Run the following command to activate python virtual environment and install all dependencies
```sh
source venv/bin/activate
pip install -r requirements.txt
```

To deactivate from virtual environment, simply run
```sh
deactivate
```

## Data Crawling
Run the command
```sh
python crawl.py
```
## Data processing
Run the command to generate airport, flight and ticket csv. Make sure they do not currently exist in the data directory before running
Also make sure flight_data.txt does not exist in current directory
```sh
python processData.py
```