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

## Selenium Setup
Download chromedriver from https://chromedriver.chromium.org/downloads and put it in this folder
<br>
Uncomment the corresponding line in crawl.py depending on your OS
```python
# driver = webdriver.Chrome('./chromedriver.exe') # windows
# driver = webdriver.Chrome('./chromedriver') # mac or linux
```

## Data Crawling
Run the command
```sh
python crawl.py
```
