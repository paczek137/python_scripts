#!/usr/bin/env python3

import requests
from bs4 import BeautifulSoup
import json
import datetime
from itertools import combinations

MAP_OF_ADJACENT_COURTS = {
    '1': [],
    '2': [],
    '3': ['4', '9'],
    '4': ['3', '5', '9'],
    '5': ['4', '6'],
    '6': ['5', '10', '13'],
    '7': ['8'],
    '8': ['7', '9'],
    '9': ['3', '4', '8'],
    '10': ['6', '11'],
    '11': ['10', '12'],
    '12': ['11'],
    '13': ['6', '14'],
    '14': ['13', '15'],
    '15': ['14'],
    '16': ['17', '18', '19'],
    '17': ['16', '18', '19'],
    '18': ['16', '17', '19'],
    '19': ['16', '17', '18'],
    '20': ['21', '30', '31'],
    '21': ['20', '22', '29', '30'],
    '22': ['21', '23', '28', '29'],
    '23': ['22', '27', '28'],
    '24': ['25'],
    '25': ['24', '26'],
    '26': ['25', '27'],
    '27': ['23', '26', '28'],
    '28': ['22', '23', '27', '29'],
    '29': ['21', '22', '28', '30'],
    '30': ['20', '21', '29', '31'],
    '31': ['20', '30', '32'],
    '32': ['31']
}

class Court:
    def __init__(self, id):
        self.id = id
        self.timetable={}
        # print("Created court no: " + str(id))

    def AddTimetableEntry(self, time, is_free):
        self.timetable[time] = is_free

    def IsFreeAtHour(self, time):
        return self.timetable[time] if time in self.timetable else False

    def IsAdjacentToCourt(self, court):
        if MAP_OF_ADJACENT_COURTS[self.id]:
            return court.id in MAP_OF_ADJACENT_COURTS[self.id]
        if MAP_OF_ADJACENT_COURTS[court.id]:
            return self.id in MAP_OF_ADJACENT_COURTS[court.id]
        return False

def getTimeTable(date_and_time):
    url = "https://hastalavista.pl/rezerwacje/"
    url_php = 'https://hastalavista.pl/wp-admin/admin-ajax.php'
    # date='2025-02-06'
    date=date_and_time.strftime("%Y-%m-%d")
    timeStart='16:00'
    timeEnd='00:00'
    #operacja=ShowRezerwacjeTable&action=ShowRezerwacjeTable&data=2025-02-06&obiekt_typ=squash&godz_od=&godz_do=
    form = {'operacja': 'ShowRezerwacjeTable',
            'action': 'ShowRezerwacjeTable',
            'data': date,
            'obiekt_typ': 'squash',
            'godz_od': timeStart,
            'godz_do': timeEnd}

    session = requests.Session()
    req = session.get(url)
    req = session.post(url_php, data=form)

    # print(req.content)
    with open("hasta.html", "w") as file:
        file.write(req.text)

def parseTimeTable(content):
    print("parsing...")
    courts = []
    soup = BeautifulSoup(content, "html.parser")
    courtClass = soup.find_all('div', class_='court court--')
    courtClass.extend(soup.find_all('div', class_='court court--space'))
    print("found " + str(len(courtClass)) + " court classes")

    for court in courtClass:
        # get number of the court
        c = Court(id=court.find('div', class_='court__number court__number--left').text)
        for item in court.find_all('div', class_='court__item-wrapper court__item-wrapper--'):
            hour = item.find('div', class_='court__hour').text
            # print(item)
            if item.find(class_="court__input court__input--free") is not None:
                is_free_court = True
            else:
                is_free_court = False
            c.AddTimetableEntry(hour, is_free_court)

        courts.append(c)
    courts.sort(key=lambda c : int(c.id))
    return courts

def checkIfAnyCourtIsFreeAtHour(courts, date_and_time, play_time=60):
    res = []
    hours = []
    
    for interval in range(0, play_time, 30):
        hours.append((date_and_time + datetime.timedelta(minutes=interval)))

    for court in courts:
        if all(court.IsFreeAtHour(hour.strftime("%H:%M")) for hour in hours):
            res.append(court)
    if not res:
        print("Not found any free courts at: " + date_and_time.strftime("%H:%M") + " for " + str(play_time) + " minutes")
        return
    s = ", ".join(str(r.id) for r in res)
    print("Found free courts: " + s + " at " + date_and_time.strftime("%H:%M") + " for " + str(play_time) + " minutes")
    checkIfCourtsAreAdjacent(res, 3)

def checkIfCourtsAreAdjacent(courts, number_of_courts=2):
    combinationList = list(combinations(courts, number_of_courts))
    for combinationCourt in combinationList:
        s = ", ".join(str(c.id) for c in combinationCourt)
        # print("combination of " + s)
    listOfCourtSets = []
    for comb in combinationList:
        firstCourt = comb[0]
        found = True
        i=1
        for court in comb[1:]:
            if not any(court.IsAdjacentToCourt(alreadyCheckedCourt) for alreadyCheckedCourt in comb[:i]):
            # if not firstCourt.IsAdjacentToCourt(court):
                found = False
                # print("failed to check " + str(firstCourt.id) + " and " + str(court.id))
                break
            firstCourt = court
            i = i + 1
        if found:
            listOfCourtSets.append(comb)

    print("found " + str(len(listOfCourtSets)) + " sets")
    for courtSet in listOfCourtSets:
        s = ", ".join(str(c.id) for c in courtSet)
        print("Found set of " + str(number_of_courts) + " courts: " + s)

    return True


def main() -> None:
    # date_and_time = datetime.datetime(2025, 2, 6, 19, 0)
    date_and_time = datetime.datetime(2025, 2, 6, 20, 0)

    # getTimeTable(date_and_time)
    courts = parseTimeTable(open("hasta.html", "r").read())
    checkIfAnyCourtIsFreeAtHour(courts, date_and_time)

if __name__ == '__main__':
    main()
