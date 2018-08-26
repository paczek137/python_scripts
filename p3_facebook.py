import datetime
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

s = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]
s = s + "\np3_facebook.py"
print(s)

'''
driver = webdriver.Firefox()
driver.get("http://www.python.org")

assert "Python" in driver.title
print(driver.title)

elem = driver.find_element_by_name("q")
elem.clear()
elem.send_keys("pycon")
elem.send_keys(Keys.RETURN)
assert "No results found." not in driver.page_source

driver.close()

'''

login =  "+48782143060"
password = "qwerty0987"

driver = webdriver.Firefox()
driver.get("https://www.facebook.com/")
print("Opened facebook")

a = driver.find_element_by_id('email')
a.send_keys(login)
b = driver.find_element_by_id('pass')
b.send_keys(password)
c = driver.find_element_by_id('loginbutton')
c.click()

