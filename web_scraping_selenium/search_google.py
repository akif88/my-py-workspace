from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait # available since 2.4.0
from selenium.webdriver.support import expected_conditions as EC # available since 2.26.0
from selenium.webdriver.common.by import By


# Create a new instance of the Firefox driver
driver = webdriver.Chrome()

# go to the google home page
# driver.get("https://www.seleniumhq.org/docs/03_webdriver.jsp")
driver.get("https://www.sahibinden.com/alfa-romeo")

print(driver.title)

"""
# name attribute is q (the google search box)
inputElement = driver.find_element_by_name("q")
inputElement.send_keys("cheese!")
inputElement.submit()
"""

"""
# element = driver.find_element_by_id("asd")
# or
element = driver.find_element(by=By.ID, value="asd")


# cheeses = driver.find_elements_by_class_name("cheese")
# or
cheese = driver.find_element(By.CLASS_NAME, "cheese")


# the DOM tag
# frame = driver.find_element_by_tag_name("iframe")
# or
frame = driver.find_element(By.TAG_NAME, "iframe")


# <input name="cheese" type="text"/>
# cheese = driver.find_element_by_name("cheese")
# or
cheese = driver.find_element(By.NAME, "cheese")


# <a href="http://www.google.com/search?q=cheese">cheese</a>
# cheese = driver.find_element_by_link_text("cheese")
# or
cheese = driver.find_element(By.LINK_TEXT, "cheese")


# <div id="food"><span class="dairy">milk</span><span class="dairy aged">cheese</span></div>
# cheese = driver.find_element_by_css_selector("#food span.dairy.aged")
# or
cheese = driver.find_element(By.CSS_SELECTOR, "#food span.dairy.aged")
"""

# inputs = driver.find_elements_by_xpath("//input")
# or
# inputs = driver.find_elements(By.XPATH, "//input")

import time
try:
    # att=WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, "input")))
    att = driver.find_elements(By.XPATH, "//*[@id=\"searchResultsTable\"]/tbody/tr/td[2]")
    # att = driver.find_elements(By.TAG_NAME, "td")
    time.sleep(10)
    #print(type(att), type(att.get_attribute("src")))
    
    for at in att:
        # print(at.get_attribute("value"))
        # print(at.get_attribute("innerHTML"))
        print(at.text)
     
    
    # print(att.get_attribute("type"))
    print(driver.title)
finally:
    driver.quit()
   # body > a
   # searchResultsTable > tbody > tr:nth-child(1) > td:nth-child(2)
   #*[@id="searchResultsTable"]/tbody/tr[1]/td[4]
   #//*[@id="searchResultsTable"]/tbody/tr[1]/td[2]
