import json
from datetime import datetime

from sqlite.sqlite_attendance import insAttendanceRecordStmt
from sqlite.sqlite_procs import UpdDataWithArgs
from sqlite.sqlite_schedule import GetClassRecords
from blueprints.students.sqlite_students import GetSqliteStudents

def validateCheckin(receivedData: any):
    receivedData['needsClassConfirmation'] = 'Y'
    receivedData['needsRankConfirmation']  = 'Y'
    if receivedData['badgeNumber'] is None or receivedData['badgeNumber'] == '':
        return {
            "message": "No badge number was entered!",
            "status" : "error",
            "class"  : "text-danger",
            "received_data": receivedData
        }

    studentData = verifyBadgeNumber(receivedData)
    if studentData is None:
        return {
            "message": "No student found for that badge number!",
            "status": "error",
            "class": "text-danger",
            "received_data": receivedData
        }

    if studentData['currentRankNum'] is not None:
        receivedData['needsRankConfirmation'] = 'N'

    classData = verifyCheckinDateTime()

    # check for already checked in for the day
    
    #save checkin record
    checkinData = saveCheckinRecord(receivedData, studentData, classData)

    if classData is None:
        return {
            "message": "No classes are available for this time!",
            "status": "error",
            "class": "text-danger",
            "received_data": receivedData
        }
    else:
        return {
            "message": "Data received successfully!",
            "status": "success",
            "class": "text-success",
            "received_data": receivedData,
            "classData": classData,
        }

def saveCheckinRecord(receivedData: dict, studentData: dict, classData: dict):
    print(f'receivedData: {json.dumps(receivedData)}')
    # print(f'studentData: {json.dumps(studentData)}')
    print(f'classData: {json.dumps(classData)}')

    try:
        currentTime = datetime.now()
        checkinDateTime = currentTime.strftime("%Y-%m-%d %H:%M:%S")
        checkinDate     = currentTime.strftime("%m/%d/%Y")
        checkinTime     = currentTime.strftime("%I:%M %p")

        attendanceRecord = {
            'badgeNumber'      : studentData['badgeNumber'],
            'checkinDateTime'  : checkinDateTime,
            'checkinDate'      : checkinDate,
            'checkinTime'      : checkinTime,
            'studentFirstName' : studentData['firstName'],
            'studentLastName'  : studentData['lastName'],
            'studentStatus'    : studentData['status'],
            'studentRankNum'   : studentData['currentRankNum'],
            'studentRankName'  : studentData['currentRankName'],
            'studentStripeId'  : studentData['currentStripeId'],
            'studentStripeName': studentData['currentStripeName'],
            'classNum'         : classData['classNum'] if classData else None,
            'className'        : None,
            'classStartTime'   : classData['classStartTime'] if classData else None,
            'styleNum'         : classData['styleNum'] if classData else None,
            'appliesPromotion' : classData['isPromotions'] if classData else None,
        }
        insStmt = insAttendanceRecordStmt()
        UpdDataWithArgs(insStmt, attendanceRecord)

        return None
    except Exception as ex:
        print(f'saveCheckinRecord error: {ex.__str__()}')
        return None

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
    dayNumber       = 0 if dayNumber > 6 else dayNumber
    currentTime     = currentDatetime.time()

    classesByDay = [x for x in classRecords if str(x['classDayOfWeek']) == str(dayNumber)]
    for classRecord in classesByDay:
        if str(classRecord['classDayOfWeek']) == str(dayNumber):
            classCheckinTimeStart = datetime.strptime(classRecord['classCheckinStart'], "%H.%M").time()
            classCheckinTimeFinis = datetime.strptime(classRecord['classCheckInFinis'], "%H.%M").time()

            classTimeStart = datetime.strptime(classRecord['classStartTime'], "%I:%M %p").time()
            classTimeFinis = datetime.strptime(classRecord['classFinisTime'], "%I:%M %p").time()

            if (   classCheckinTimeStart <= currentTime <= classCheckinTimeFinis
                or classTimeStart <= currentTime <= classTimeFinis):
                return classRecord

    return getClosestClasses(currentDatetime, classesByDay)
    # return classesByDay[-1]
    # return None

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