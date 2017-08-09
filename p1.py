import datetime

s = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]
print(s)