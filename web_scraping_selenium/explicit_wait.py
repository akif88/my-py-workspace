from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait # available since 2.4.0
from selenium.webdriver.support import expected_conditions as EC # available since 2.26.0

ff = webdriver.Firefox()
ff.get("https://www.imdb.com/awards-central/?ref_=nv_tp_awrd")
try:
    element = WebDriverWait(ff, 10).until(EC.presence_of_element_located((By.TAG_NAME, "html")))
    content = element.get_attribute("innerHTML")
    print(content)
    
finally:
    ff.quit()
