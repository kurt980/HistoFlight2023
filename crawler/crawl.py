from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

url = 'https://www.google.com/travel/flights?q=Flights%20to%20ORD%20from%20LAX%20on%202022-10-13%20one%20way%20nonstop'

# driver = webdriver.Chrome('./chromedriver.exe') # windows
# driver = webdriver.Chrome('./chromedriver') # mac or linux
driver.get(url)

WebDriverWait(driver, 10).until(
EC.presence_of_element_located((By.CLASS_NAME, "YMlIz"))
)

elements = driver.find_elements(By.XPATH, "//li[not(@role='option')]")

outF = open("flight_data.txt", "w")

for el in elements:
    outF.write(el.text)
    outF.write('\n\nseperator\n\n')

driver.quit()
outF.close()
