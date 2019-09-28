# author: paczek

import datetime
import os
import requests
from bs4 import BeautifulSoup

s = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]
s = s + "\n" + os.path.basename(__file__)
print(s)


def wagon_find_menu():
    url_base = "https://m.facebook.com/"
    url = url_base + "Wagonowa"
    page = requests.get(url)
    soup = BeautifulSoup(page.content, "html.parser")

    spans = soup.find_all('span')
    for span in spans:
        if "ZUPA" in span.text:
            print("found!")
            zupa = span
            break
    #print(zupa.text)

    link = zupa.find('a')
    link = url_base + link['href'][1:]
    print(link)

    page2 = requests.get(link)
    soup2 = BeautifulSoup(page2.content, "html.parser")
    menu = soup2.title
    print(menu.text)
    return menu.text

if __name__ == '__main__':
    wagon_find_menu()