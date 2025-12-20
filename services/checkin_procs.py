from datetime import datetime

from sqlite.sqlite_schedule import GetClassRecords
from blueprints.students.sqlite_students import GetSqliteStudents

def validateCheckin(data: any):
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

    classData = verifyCheckinDateTime(data)
    if classData is None:
        return {
            "message": "No services are available for this time!",
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

def verifyCheckinDateTime(data):
    classRecords    = GetClassRecords()
    currentDatetime = datetime.now()
    dayNumber   = currentDatetime.weekday() + 1
    currentTime = currentDatetime.time()

    classesByDay = [x for x in classRecords if str(x['classDayOfWeek']) == str(dayNumber)]
    for classRecord in classesByDay:
        if str(classRecord['classDayOfWeek']) == str(dayNumber):
            classCheckinTimeStart = datetime.strptime(classRecord['classCheckinStart'], "%H.%M").time()
            classCheckinTimeFinis = datetime.strptime(classRecord['classCheckInFinis'], "%H.%M").time()
            if classCheckinTimeStart <= currentTime <= classCheckinTimeFinis:
                return classRecord
    return classesByDay[-1]
    #return None