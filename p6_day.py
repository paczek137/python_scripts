import datetime, requests

s = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]
s = s + "\np2_html_parse.py"
print(s)

day = datetime.datetime.today().weekday()

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

page = requests.get('https://www.facebook.com/pg/Wagonowa/posts/?ref=page_internal')