import datetime
import p11_facebook_parser as wagon

s = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]

print(s)

print(wagon.wagon_find_menu())