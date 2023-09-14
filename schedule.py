import datetime
import scheduleService as ss

today = datetime.date.today()


def getThisWeekSchedule():
    lessons = ss.load_all()
    week = []
    for l in lessons:
        income_date = datetime.datetime.strptime(l['date'], "%Y-%m-%d").date()
        if income_date >= today and (abs(today - income_date)).days < 7:
            week.append(l)
    return sortSchedule(week)


def getAllSchedule():
    lessons = ss.load_all()
    all = []
    for l in lessons:
        income_date = datetime.datetime.strptime(l['date'], "%Y-%m-%d").date()
        if income_date >= today:
            all.append(l)
    return sortSchedule(all)

def sortSchedule(data = []):
    for i in range(len(data) - 1):
        for j in range(len(data) - i - 1):
            if data[j]['date'] > data[j + 1]['date']:
                bigger = data[j + 1]
                data[j + 1] = data[j]
                data[j] = bigger
    return data

