import json
import os
import sys
import requests
import winsound
import time


url = "https://kl570.elaborat.marcel.pl/index.php?cmd=logowanie&barcodeLogin=true"
params = {
    "barcode": "2042485320",
    "pesel": "92061113119",
    "day": "11",
    "month": "06",
    "year": "1992",
    "changeBarcode": "on"
}

error_message = "Dane nie są zarejestrowane w systemie eLaborat lub są niepoprawne."
r = requests.post(url, data=params)
#print(r.headers)
#print(r.text)

if error_message in r.text:
    print("No covid results")
else:
    print("There could be covid results .. or some error")


#f = open("pages/covid_res.html","wb")
#f.write(r.text.encode("utf-8"))
#f.close()