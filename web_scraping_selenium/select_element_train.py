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
#driver.get("http://www.cumhuriyet.com.tr/bolum/38/basketbol.html")

print(driver.title)

import time
try:
    #element = driver.execute_script("return $('.searchResultsRowClass')")
    #print(type(element))
    #print(element)
    
    asd=""
    #asd = driver.find_elements_by_tag_name("td")
    inputs = driver.execute_script("""
             
            
             var prt = $("*", document.body).on('click', function(e){
                        var parentTag = $(this).parents().map(function(){
                            return this.tagName;
                        }).get().join(", ");                        
                        
                        return parentTag;
                    });
            

             return prt;     
     """)

                  #var td = this.cellIndex;\
                  #alert(td);\
    
    
    time.sleep(10)
    
    #print(type(asd))
    #print(asd)
    #print(asd.get_attribute("innerHTML"))

    print(type(inputs))
    print(inputs.text)
    #print(asd)
    for i in inputs:
        print(i.get_attribute("innerHTML"))



    #print(inputs.get_attribute("id"))
    #print(type(inputs))

    #for i in inputs:
        #print(i.get_attribute("innerHTML"))

    #for i in element:
    #    print(i.get_attribute("innerHTML"))

    #att = driver.find_elements(By.XPATH, "/body/div/div/form/div/div/table/tbody/tr/td[1]")
    
    
    #for i in att:
    #    print(i.text)
     
    time.sleep(20)
    print(driver.title)
finally:
    driver.quit()
