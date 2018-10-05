import datetime, time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions

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

login =  "+48516022766"
password = "qwerty0987"

fp = webdriver.FirefoxProfile()
fp.set_preference("permissions.default.desktop-notification", 0)
fp.set_preference("dom.webnotifications.enabled", False)
#cap = webdriver.DesiredCapabilities.FIREFOX.copy()



driver = webdriver.Firefox(firefox_profile=fp)
driver.get("https://www.facebook.com/")
print("Opened facebook")
driver.maximize_window()


a = driver.find_element_by_id('email')
print(a)
#aa = driver.find_element(By.CSS_SELECTOR, '#m_login_email')
aa = driver.find_element_by_xpath('//*[@id="email"]')
print(aa)
a.send_keys(login)
b = driver.find_element_by_id('pass')
b.send_keys(password)
c = driver.find_element_by_id('loginbutton')
c.click()


#driver.get("https://www.facebook.com/groups/1888323521464203/")
driver.get("https://www.facebook.com/groups/288421491988781/")
driver.execute_script("window.scrollTo(0, 500);")

#for writting on the wall
#wall = driver.find_element_by_xpath("//textarea[@name='xhpc_message']")
#time.sleep(5)
#p = driver.find_element_by_xpath("//textarea[@name='message']")
p = driver.find_element_by_name('xhpc_message_text')
#p.screenshot('C:\git\python\python_scripts\p1.png')

p.send_keys('paczek test4')

time.sleep(1)
element = WebDriverWait(driver, 30).until(expected_conditions.element_to_be_clickable((By.XPATH, '//button/span[.=\"Post\"]')))
#element = WebDriverWait(driver, 30).until(expected_conditions.element_to_be_clickable((By.XPATH, "//span[text()='Post']")))
element.screenshot('C:\git\python\python_scripts\p2.png')

element.click()

#postbutton = driver.find_element_by_xpath("//button[contains(.,'Post')]")
#postbutton.click()
