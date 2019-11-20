import datetime, requests, time
from bs4 import BeautifulSoup
import ctypes
import winsound

s = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]
s = s + "\np8_hasta_post.py"
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

def parse_timetables2(source, at_time):
    # soup = BeautifulSoup(driver.page_source, "html.parser")
    # file = open("view-source_hastalavista.pl_online_rezerwacje_.html", "r")
    # content = file.read()
    # file.close()
    soup = BeautifulSoup(source, "html.parser")

    courts = []
    table = soup.find('table', 'rez')
    tr_count = 0
    for tr in table.find_all('td', 'rez rez_wolne'):
        tr_count = tr_count + 1
        at_time_free = tr.input["data-godz_od"]
        if at_time_free == at_time:
            #print("Found new court")
            court_number = get_real_court_number(int(tr.parent['data-obie_id']))
            courts.append(str(court_number))
            print("Added court: " + str(court_number))

    print("Free courts at " + at_time + ": " + str(courts))
    print("Done")
    return courts


url = "http://hastalavista.pl/online/rezerwacje/"
data = "operacja=ShowRezerwacjeTable&action=ShowRezerwacjeTable&data=2019-05-26&obiekt_typ=squash&godz_od=&godz_do="
data2 = {'operacja':'ShowRezerwacjeTable', 'action':'ShowRezerwacjeTable', 'data':'019-05-26', 'obiekt_typ':'squash', 'godz_od':'', 'godz_do':''}
#cookie = "godz_do=00%3A00; godz_od=15%3A00; obiekt_typa=squash; qtrans_cookie_test=1"
cookie = "obiekt_typa=squash; qtrans_cookie_test=1; godz_od=15%3A00; godz_do=00%3A00; obiekt_typa=squash; __utma=205523210.1690845683.1558640193.1558640193.1558640193.1; __utmc=205523210; __utmz=205523210.1558640193.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none); __utmt=1; __utmb=205523210.1.10.1558640193; viewed_cookie_policy=yes"


test_url = "https://httpbin.org/post"
url_php = "http://hastalavista.pl/wp-admin/admin-ajax.php"
form = {'operacja': 'ShowRezerwacjeTable', 'action': 'ShowRezerwacjeTable',
        'data': '2019-11-13', 'obiekt_typ': 'squash',
        'godz_od': '15:00', 'godz_do': '00:00'}


s = requests.Session()
r = s.get(url)
#s.headers.update({'host': 'hastalavista.pl'})
r = s.post(url_php, data=form)

#print(r.request.headers)
#print(r.headers)
# print(r.text)
#f = open("pages/h.html","wb")
#f.write(r.content)
#f.close()

courts = parse_timetables2(r.content, "20:00")
#print(courts)
if len(courts) > 0:
    print("OK")
    winsound.MessageBeep()
    ctypes.windll.user32.MessageBoxW(0, "Free courts: " + str(courts), "Alert", 0)
else:
    print("No free courts found")