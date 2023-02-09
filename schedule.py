import csv
import datetime

today = datetime.date.today()


def getThisWeekSchedule(csv_lines):
    week = []
    for line in csv_lines:
        income_date = datetime.datetime.strptime(line[0], "%d.%m.%Y").date()
        if income_date >= today and (abs(today - income_date)).days < 7:
            week.append(line)

    return week


def getAllSchedule(csv_lines):
    all = []
    for line in csv_lines:
        income_date = datetime.datetime.strptime(line[0], "%d.%m.%Y").date()
        if income_date >= today:
            all.append(line)

    return all


def getSchedule(file_url, week=False):
    with open(file_url, newline='', encoding="utf-8") as csvfile:
        reader = csv.reader(csvfile)
        if week:
            return getThisWeekSchedule(reader)
        else:
            return getAllSchedule(reader)

