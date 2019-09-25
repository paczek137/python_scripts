import datetime, requests
from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
from tkinter import messagebox
from seleniumrequests import Firefox

s = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]
s = s + "\np7_html_parse.py"
print(s)

#webdriver = Firefox()
#webdriver.set_page_load_timeout(20)
#driver.get("http://hastalavista.pl/online/rezerwacje/")
#operacja=ShowRezerwacjeTable&action=ShowRezerwacjeTable&data=2019-05-26&obiekt_typ=squash&godz_od=&godz_do=
#response = webdriver.request('POST', "http://hastalavista.pl/online/rezerwacje/", data={"operacja": "ShowRezerwacjeTable"})
#print(response)
#exit()

def get_real_court_number(num):
    if num >= 1 and num < 23:
        return num
    elif num >= 23 and num < 36:
        return num - 10
    elif num >= 36 and num < 54:
        return num - 16
    elif num >= 54 and num < 58:
        return num - 25

def parse_timetables(driver, at_time):
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
            if at_time in time_from:
                parent = el.find_element_by_xpath(".//..")
                #courts.append(parent.get_attribute("data-obie_id"))
                court_number = get_real_court_number(int(parent.get_attribute("data-obie_id")))
                courts.append(str(court_number))
                print("Added court " + str(court_number))
            #else:
                #print("no matching 22:00")
    else:
        print("No found slots")

    print("Free courts at " + at_time + ": " + str(courts))
    print("Done")
    return courts

def parse_timetables2(source, at_time):
    #soup = BeautifulSoup(driver.page_source, "html.parser")
    #file = open("view-source_hastalavista.pl_online_rezerwacje_.html", "r")
    #content = file.read()
    #file.close()
    soup = BeautifulSoup(source, "html.parser")

    courts = []
    table = soup.find('table', 'rez')
    tr_count = 0
    for tr in table.find_all('td', 'rez rez_wolne'):
        tr_count = tr_count + 1
        #child = tr.contents[1]
        at_time_free = tr.input["data-godz_od"]
        if at_time_free == "17:00":
            #print("Found new court")
            court_number = get_real_court_number(int(tr.parent['data-obie_id']))
            courts.append(str(court_number))
            print("Added court: " + str(court_number))

    print("Free courts at " + at_time + ": " + str(courts))
    print("Done")
    return courts


def hasta_go_to_date(driver, target_date):
    d1 = datetime.datetime.today()
    diff = datetime.timedelta(days=1)

    while True:
        current_hasta_date = driver.find_element_by_id('rez_wybrana_data').get_attribute('value')
        if current_hasta_date == target_date:
            print("Get target date: " + current_hasta_date)
            return

        button = driver.find_element_by_id("rez_data_p_b")
        button.click()

        d1 = d1 + diff
        expected_date = days[d1.weekday()] + ", " + str(d1.day) + " " + months[d1.month-1] + ", " + str(d1.year)
        print("current expected date: " + expected_date)

        wait = WebDriverWait(driver, 10)
        element = wait.until(
            EC.text_to_be_present_in_element_value((By.ID, 'rez_wybrana_data'), expected_date))

day = datetime.datetime.today().weekday()
time_now_hour = datetime.datetime.today().hour
time_now_min = datetime.datetime.today().minute
if time_now_min < 10:
    time_now_min = "0" + str(time_now_min)

days = [
    "Poniedziałek",
    "Wtorek",
    "Środa",
    "Czwartek",
    "Piątek",
    "Sobota",
    "Niedziela"
]

months = [
    "Styczeń",
    "Luty",
    "Marzec",
    "Kwiecień",
    "Maj",
    "Czerwiec",
    "Lipiec",
    "Sierpień",
    "Wrzesień",
    "Październik",
    "Listopad",
    "Grudzień"
]

print(days[day])
s = str(time_now_hour) + ":" + str(time_now_min)
print(s)

current_datetime = days[day] + ", " + str(datetime.datetime.today().day) + " " \
                   + months[datetime.datetime.today().month-1] + ", " + str(datetime.datetime.today().year)
print("Generated current date: " + current_datetime)

driver = webdriver.Firefox()
driver.set_page_load_timeout(20)
driver.get("http://hastalavista.pl/online/rezerwacje/")
current_hasta_date = driver.find_element_by_id('rez_wybrana_data').get_attribute('value')
print("Current hasta date: " + current_hasta_date)
if current_datetime == current_hasta_date:
    print("match")

target_date = "Poniedziałek, 6 Maj, 2019"
hasta_go_to_date(driver, target_date)
#button = driver.find_element_by_xpath("//button[@id='rez_data_p_b']")

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

#courts = parse_timetables(driver, at_time="17:00")
courts = parse_timetables2(driver.page_source, "17:00")
driver.quit()

if "14" in courts:
    messagebox.showinfo("Hasta La Vista", "Free court 14!")