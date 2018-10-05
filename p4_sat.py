import datetime, time

import os

import sys
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions
from selenium.common.exceptions import TimeoutException

#Datetime
DATE_AND_TIME = ('{:%Y_%m_%d_%H_%M_%S}'.format(datetime.datetime.now()))

#Dir for logs
LOG_DIR = "log"

#Filename
#LOG_FILENAME = LOG_DIR + "\\" + sys.argv[0][:-3] + "_" + DATE_AND_TIME + ".txt"
LOG_FILENAME = os.getcwd() + "\\" + LOG_DIR + "\\p4_sat_" + DATE_AND_TIME + ".txt"

print(LOG_FILENAME)

def append_to_file(text):
    f = open(LOG_FILENAME,"a")
    text = text + '\n'
    f.write(text)
    f.close()
    print(text)

def find_big_yellow(drv, code):
    y = drv.find_elements_by_xpath("//span[@style='color: yellow']")
    if len(y) > 0:
        s = 'Found ' + str(len(y)) + ' yellows at ' + driver.current_url
        append_to_file(s)

        for el in y:
            # print(el.text)
            # print(el.find_element_by_xpath("..").get_attribute('style'))
            if "font-size" in el.find_element_by_xpath("..").get_attribute('style'):
                # print(el.text)
                if len(el.text) < 20:
                    s = 'Found Code => ' + el.text + ' in URL:  ' + drv.current_url
                    append_to_file(s)
                    code.append(el.text)

def find_only_yellow(drv):
    #time.sleep(2)
    y_patter = [
        "color: yellow",
        "color:yellow",
        "color:'#FFFF00'",
        "color: '#FFFF00'",
        'color:"#FFFF00"',
        'color: "#FFFF00"'
    ]
    for idx, el in enumerate(y_patter):
        if el in drv.page_source:
            t = "Y" + str(idx) + ": " + el + " at: " + drv.current_url
            append_to_file(t)
            break




def find_last_page_in_a_href(drv, code):
    elems = drv.find_elements_by_xpath("//a[@href]")
    pages = []
    for elem in elems:
        if 'postorder' in elem.get_attribute("href"):
            #print(elem.get_attribute("href"))
            pages.append(elem.get_attribute("href"))
    #print('last page')
    #print(pages[len(pages)-2])
    #check last 2 pages
    if len(pages) > 2:
        try:
            drv.get(pages[len(pages) - 3])
            find_only_yellow(drv)
            #find_big_yellow(drv, code)
            drv.get(pages[len(pages) - 2])
            find_only_yellow(drv)
            #find_big_yellow(drv, code)
        except TimeoutException as ex:
            s = "Timeout exception " + str(ex) + " at " + driver.current_url
            append_to_file(s)
            #reset the driver
            drv.delete_all_cookies()
            drv.close()
            drv = webdriver.Firefox(firefox_profile=fp)
            login_to_sat(drv)

    else:
        find_only_yellow(drv)
        #find_big_yellow(drv, code)

def login_to_sat(drv):
    driver.get("http://satedu.2ap.pl/login.php")
    append_to_file("Opened sat-edu")
    driver.maximize_window()

    a = driver.find_element_by_name('username')
    a.send_keys(login)
    b = driver.find_element_by_name('password')
    b.send_keys(password)
    b.send_keys(u'\ue00c')
    c = driver.find_element_by_name('login')
    c.click()


if not os.path.exists(LOG_DIR):
    os.makedirs(LOG_DIR)
open(LOG_FILENAME, 'w').close()

s = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]
s = s + "\np4_sat.py"
append_to_file(s)

login =  "paczek137"
password = "widzew1910"

fp = webdriver.FirefoxProfile()
fp.set_preference("permissions.default.desktop-notification", 0)
fp.set_preference("dom.webnotifications.enabled", False)
#cap = webdriver.DesiredCapabilities.FIREFOX.copy()



driver = webdriver.Firefox(firefox_profile=fp)
login_to_sat(driver)

code_list = []

#driver.get("http://satedu.2ap.pl/index.php?c=6")
#driver.get("http://satedu.2ap.pl/viewtopic.php?t=21941")
#driver.get("http://satedu.2ap.pl/viewtopic.php?t=3260")

driver.set_page_load_timeout(30)

#814
i = 11198
end = 1
while True:
    adr = "http://satedu.2ap.pl/viewtopic.php?t=" + str(i)
    try:
        driver.get(adr)
    except TimeoutException as ex:
        s = "Timeout exception " + str(ex) + " at " + driver.current_url
        append_to_file(s)
        i = i - 1
        # reset the driver
        driver.delete_all_cookies()
        driver.close()
        driver = webdriver.Firefox(firefox_profile=fp)
        login_to_sat(driver)
        continue
    find_last_page_in_a_href(driver, code_list)
    #find_big_yellow(driver, code_list)
    i = i - 1
    if i < end:
        break

i = 0
for el in code_list:
    i = i + 1
    t = str(i) + ". " + el
    append_to_file(t)
driver.quit()
