import datetime, requests, re
from lxml import html
from bs4 import BeautifulSoup

s = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]
s = s + "\np2_html_parse.py"
print(s)

page = requests.get('http://econpy.pythonanywhere.com/ex/001.html')
tree = html.fromstring(page.content)

#This will create a list of buyers:
buyers = tree.xpath('//div[@title="buyer-name"]/text()')
#This will create a list of prices
prices = tree.xpath('//span[@class="item-price"]/text()')

print('Buyers: ', buyers)
print('Prices: ', prices)

page2 = requests.get('https://en.wikipedia.org/wiki/Administrative_divisions_of_Poland')
soup = BeautifulSoup(page2.content, 'html.parser')

voivoidship_counter = 0
td_count = 0
file = open("testfile.txt","w")

t = soup.find('table', 'wikitable')
for tr in t.find_all('tr'):
    td_count = 0
    for td in tr.find_all('td'):
        td_count = td_count + 1
        if td_count == 2:
            voivoidship_counter = voivoidship_counter + 1
            print(td.text)
            file.write("<item>")
            file.write(td.text)
            file.write("</item>\n")
    #print("td count: " + str(td_count))
print("voivoidship counter: " + str(voivoidship_counter))
file.close()







