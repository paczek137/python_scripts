import datetime, requests
from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup

s = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]
s = s + "\np7_html_parse.py"
print(s)

def get_real_court_number(num):
    if num >= 1 and num < 23:
        return num
    elif num >= 23 and num < 36:
        return num - 10
    elif num >= 36 and num < 54:
        return num - 16
    elif num >= 54 and num < 58:
        return num - 25

def parse_timetables(driver):
    #slots = driver.find_elements_by_class_name("rez rez_wolne")
    slots = driver.find_elements_by_xpath("//td[@class='rez rez_wolne']")
    courts = []
    if len(slots) > 0:
        print("Found " + str(len(slots)) + " slots")
        child = slots[0].find_element_by_xpath(".//*")
        parent = slots[0].find_element_by_xpath(".//..")
        print(child.get_attribute("data-godz_od"))
        print(child.get_attribute("data-godz_do"))
        print(parent.get_attribute("data-obie_id"))

        for el in slots:
            #print(".")
            child = el.find_element_by_xpath(".//*")
            time_from = child.get_attribute("data-godz_od")
            #print(time_from)
            #if child is not None:
            if "22:00" in time_from:
                parent = el.find_element_by_xpath(".//..")
                #courts.append(parent.get_attribute("data-obie_id"))
                court_number = get_real_court_number(int(parent.get_attribute("data-obie_id")))
                courts.append(str(court_number))
                print("Added court " + str(court_number))
            #else:
                #print("no matching 22:00")
    else:
        print("No found slots")

    print("Free courts at 22:00: " + str(courts))
    print("Done")

def parse_timetables2(driver):
    soup = BeautifulSoup(driver.page_source, "html.parser")
    table = soup.find('table', 'rez')
    tr_count = 0
    for tr in table.find_all('td', 'rez rez_wolne'):
        tr_count = tr_count + 1
    print("found " + str(tr_count) + " tr")
    print("Done")

day = datetime.datetime.today().weekday()
time_now_hour = datetime.datetime.today().hour
time_now_min = datetime.datetime.today().minute

days = [
    "poniedziałek",
    "wtorek",
    "środa",
    "czwartek",
    "piątek",
    "sobota",
    "niedziela"
]

print(days[day])
s = str(time_now_hour) + ":" + str(time_now_min)
print(s)


driver = webdriver.Firefox()
driver.set_page_load_timeout(20)
driver.get("http://hastalavista.pl/online/rezerwacje/")
#button = driver.find_element_by_xpath("//button[@id='rez_data_p_b']")
button = driver.find_element_by_id("rez_data_p_b")
button.click()

wait = WebDriverWait(driver, 10)
element = wait.until(EC.text_to_be_present_in_element_value((By.ID, 'rez_wybrana_data'), "Czwartek, 18 Kwiecień, 2019"))

hasta_date = driver.find_element_by_id("rez_wybrana_data").get_attribute('value')
print(hasta_date)
radios = driver.find_elements_by_name("radio")
if len(radios) > 0:
    print("Found " + str(len(radios)) + " radios")
    for el in radios:
        if el.is_selected():
            print(el.get_attribute('id') + " is selected")
        else:
            print(el.get_attribute('id'))
else:
    print("No radios")

parse_timetables(driver)
#parse_timetables2(driver)

driver.quit()