from datetime import datetime

from sqlite.sqlite_schedule import GetClassRecords
from blueprints.students.sqlite_students import GetSqliteStudents

def validateCheckin(data: any):
    data['needsClassConfirmation'] = 'Y'
    data['needsRankConfirmation']  = 'Y'
    if data['badgeNumber'] is None or data['badgeNumber'] == '':
        return {
            "message": "No badge number was entered!",
            "status" : "error",
            "class"  : "text-danger",
            "received_data": data
        }

    studentData = verifyBadgeNumber(data)
    if studentData is None:
        return {
            "message": "No student found for that badge number!",
            "status": "error",
            "class": "text-danger",
            "received_data": data
        }

    classData = verifyCheckinDateTime()
    if classData is None:
        return {
            "message": "No classes are available for this time!",
            "status": "error",
            "class": "text-danger",
            "received_data": data
        }

    return {
        "message": "Data received successfully!",
        "status": "success",
        "class": "text-success",
        "received_data": data,
        "classData": classData,
    }

def verifyBadgeNumber(data):
    studentRecords = GetSqliteStudents()
    foundRecords   = [x for x in studentRecords if str(x['badgeNumber']) == str(data['badgeNumber'])]
    if len(foundRecords) == 1:
        return foundRecords[0]
    else:
        return None

def verifyCheckinDateTime():
    classRecords    = GetClassRecords()
    currentDatetime = datetime.now()
    dayNumber       = currentDatetime.weekday() + 1
    currentTime     = currentDatetime.time()

    classesByDay = [x for x in classRecords if str(x['classDayOfWeek']) == str(dayNumber)]
    for classRecord in classesByDay:
        if str(classRecord['classDayOfWeek']) == str(dayNumber):
            classCheckinTimeStart = datetime.strptime(classRecord['classCheckinStart'], "%H.%M").time()
            classCheckinTimeFinis = datetime.strptime(classRecord['classCheckInFinis'], "%H.%M").time()

            if classCheckinTimeStart <= currentTime <= classCheckinTimeFinis:
                return classRecord
            else:
                return getClosestClasses(currentDatetime, classesByDay)
    #return classesByDay[-1]
    return None

def getClosestClasses(currentDatetime: datetime, classesByDay: list[dict]):
    if len(classesByDay) == 0:
        return None

    currentTime     = currentDatetime.time()

    firstClass = classesByDay[0]
    firstCheckinTimeStart = datetime.strptime(firstClass['classCheckinStart'], "%H.%M").time()
    firstCheckinTimeFinis = datetime.strptime(firstClass['classCheckInFinis'], "%H.%M").time()

    lastClass = classesByDay[-1]
    lastCheckinTimeStart = datetime.strptime(lastClass['classCheckinStart'], "%H.%M").time()
    lastCheckinTimeFinis = datetime.strptime(lastClass['classCheckInFinis'], "%H.%M").time()

    # if no classes before:
    if currentTime <= firstCheckinTimeStart:
        # classesByDay[0]['needsClassConfirmation'] = 'Y'
        return classesByDay[0]

    # if no classes after
    if currentTime > lastCheckinTimeFinis:
        # classesByDay[-1]['needsClassConfirmation'] = 'Y'
        return classesByDay[-1]

    #    return classesByDay[0]