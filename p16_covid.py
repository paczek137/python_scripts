import json
import os
import sys
import requests
import winsound
import time


date = "27-10-2020"
url_appointment = "https://sklep.damian.pl/api/ext/appointments/search"
params = {
    "region_id": "[2]199",
    "product_id": "117592",
    "location_ids": "2086",
    "date_from": date,
    "sort": "true"
}

while (True):
    r = requests.post(url_appointment, json=params)
    #print(r.text)
    rson = r.json()

    target_date = rson["result"]["visits"][date]
    if target_date:
        print("There are available slot(s)!")
        for slot in target_date:
            print(slot["time"])
        #print(target_date[0]["time"])
        #winsound.Beep(440, 2000)
        #winsound.MessageBeep()
        break
    else:
        print("Nope..")
    time.sleep(30)
#print()

#f = open("pages/covid.html","wb")
#f.write(r.text.encode("utf-8"))
#f.close()