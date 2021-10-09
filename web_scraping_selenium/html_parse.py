from pyquery import PyQuery as pq
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys


driver = webdriver.Chrome()
driver.get("https://www.sahibinden.com/alfa-romeo")
print(driver.title)

try:
    html=WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, "html")))
    html_pq = html.get_attribute("innerHTML")

    html_pq = pq(html_pq)
    
    # print(html_pq)
finally:
    driver.quit()

