from datetime import datetime, date, time, timedelta

import json
from time import strptime, strftime

from sqlite.sqlite_schedule import GetClassRecordsSorted, InsertNewClass
from sqlite.sqlite_styles import GetStyleRecords


# ---------------------------------------------------------------------------------------------------
def validateClassFieldsUpdate(classData):
    validationResults = {}
    # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    inpClassName = getFieldValue(classData, 'inpClassName')
    validationResults['inpClassName'] = validateClassName(inpClassName)
    # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    errCount = len({k: v for k, v in validationResults.items() if v['status'] == 'error'})
    if errCount == 0:
        validationResults['validationResults'] = {'status': 'ok', 'message': 'Class changes have been saved'}
    else:
        validationResults['validationResults'] = {'status': 'error', 'message': f'Validation error count{errCount}'}
    return validationResults


# ---------------------------------------------------------------------------------------------------
def validateClassFieldsInsert(classData):
    validationResults = {}
    # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    inpClassName = getFieldValue(classData, 'inpClassName')
    validationResults['inpClassName'] = validateClassName(inpClassName)
    # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    inpStartTime = getFieldValue(classData, 'inpStartTime')
    validationResults['inpStartTime'] = validateClassStartTime(classData, inpStartTime)
    # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    inpClassDuration = getFieldValue(classData, 'inpClassDuration')
    validationResults['inpClassDuration'] = validateClassDuration(inpClassDuration)
    # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    chkAmPm = getFieldValue(classData, 'chkAmPm')
    validationResults['inpFinisTime'] = calculateFinisTime(chkAmPm, validationResults['inpStartTime'], validationResults['inpClassDuration'])
    # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    validationResults['classOverLap'] = checkForClassOverLap(
        classData,
        validationResults['inpStartTime'],
        validationResults['inpClassDuration'],
        validationResults['inpFinisTime']
    )
    # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    errCount = len({k: v for k, v in validationResults.items() if v['status'] == 'error'})
    if errCount == 0:
        validationResults['validationResults'] = {'status': 'ok', 'message': 'Class changes have been saved'}
    else:
        validationResults['validationResults'] = {'status': 'error', 'message': f'Validation error count{errCount}'}
    # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    return validationResults

# ---------------------------------------------------------------------------------------------------
def getFieldValue(classData, fieldName):
    fieldEntry = [x for x in classData if x['name'] == fieldName]
    if len(fieldEntry) > 0:
        return fieldEntry[0]['value']
    else:
        return None

# ---------------------------------------------------------------------------------------------------
def checkForClassOverLap(classData, vldStartTime, vldClassDuration, vldFinisTime):
    if vldStartTime['status'] == 'error' or vldClassDuration['status'] == 'error':
        return {'status': 'err', 'message': 'Could not check for overlap'}
    slctDayOfWeek = getFieldValue(classData, 'slctDayOfWeek')
    classRecords  = GetClassRecordsSorted()
    classesByDay  = [x for x in classRecords if str(x['classDayOfWeek']) == str(slctDayOfWeek)]
    if len(classesByDay) == 0:
        try:
            return {'status' : 'ok','message': 'No overlap was found', 'value' : ''}
        except Exception as ex:
            return {'status': 'error', 'message': ex.__str__(), 'value': ''}

    # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    # if start time between any other start / end time then it overlaps
    date_string     = "01-Jan-1900 " + vldStartTime['value']
    tempStartTime   = datetime.strptime(date_string, "%d-%b-%Y %I:%M %p")
    for classEntry in classesByDay:
        classStartTime = datetime.strptime("01-Jan-1900 " + classEntry['classStartTime'], "%d-%b-%Y %I:%M %p")
        classFinisTime = datetime.strptime("01-Jan-1900 " + classEntry['classFinisTime'], "%d-%b-%Y %I:%M %p")
        if classStartTime <= tempStartTime <= classFinisTime:
            return {'status': 'error', 'message': 'Class overlaps another class', 'value': classEntry['classNum']}

    # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

    return {'status' : 'ok','message': 'No overlap was found', 'value' : ''}

def getSqlClassInsertDict(classData, vldStartTime, vldClassDuration, vldFinisTime):
    return {
        'className'      : getFieldValue(classData, 'inpClassName'),
        'styleNum'       : getFieldValue(classData, 'slctStyleNum'),
        'styleName'      : getStyleName(getFieldValue(classData, 'slctStyleNum')),
        'classDayOfWeek' : getFieldValue(classData, 'slctDayOfWeek'),
        'classStartTime' : vldStartTime['value'],
        'classFinisTime' : vldFinisTime['value'],
        'classDuration'  : vldClassDuration['value'],
        'allowedRanks'   : getSelectedRanksAsString(classData),
        'classDisplayTitle' : getFieldValue(classData, 'inpClassName'),
        'allowedAges'       : getFieldValue(classData, 'inpAllowedAges'),
        'isPromotions' : getFieldValue(classData, 'chkApplies')
    }

def getSqlClassUpdateDict(classData):
    return {
        'classNum'       : getFieldValue(classData, 'classNum'),
        'className'      : getFieldValue(classData, 'inpClassName'),
        'styleNum'       : getFieldValue(classData, 'slctStyleNum'),
        'styleName'      : getStyleName(getFieldValue(classData, 'slctStyleNum')),
        # 'classDayOfWeek' : getFieldValue(classData, 'slctDayOfWeek'),
        # 'classStartTime' : vldStartTime['value'],
        # 'classFinisTime' : vldFinisTime['value'],
        # 'classDuration'  : vldClassDuration['value'],
        'allowedRanks'   : getSelectedRanksAsString(classData),
        'classDisplayTitle' : getFieldValue(classData, 'inpClassName'),
        'allowedAges'       : getFieldValue(classData, 'inpAllowedAges'),
        'isPromotions': getFieldValue(classData, 'chkApplies')
    }

def getSelectedRanksAsString(classData):
    rtnList = []
    if getFieldValue(classData, 'chkWhite')  : rtnList.append('1')
    if getFieldValue(classData, 'chkOrange') : rtnList.append('2')
    if getFieldValue(classData, 'chkYellow') : rtnList.append('3')
    if getFieldValue(classData, 'chkBlue')   : rtnList.append('4')
    if getFieldValue(classData, 'chkGreen')  : rtnList.append('5')
    if getFieldValue(classData, 'chkPurple') : rtnList.append('6')
    if getFieldValue(classData, 'chkBrown')  : rtnList.append('7')
    if getFieldValue(classData, 'chkBlack')  : rtnList.append('8')
    return ','.join(rtnList)

# ---------------------------------------------------------------------------------------------------
def getStyleName(styleNum):
    styleRecords = GetStyleRecords()
    styleNameEntry = [x for x in styleRecords if str(x['styleNum']) == str(styleNum)][0]
    return styleNameEntry['styleName']


# ---------------------------------------------------------------------------------------------------
def validateClassName(inpClassName):
    if inpClassName:
        return {'status' : 'ok','message': 'inpClassName was valid'}
    else:
        return {'status' : 'error','message': 'Class name is a required field'}

# ---------------------------------------------------------------------------------------------------
def validateClassStartTime(classData, inpStartTime):
    if inpStartTime:
        chkAmPm   = getFieldValue(classData, 'chkAmPm')
        startTime = validate_time_format(inpStartTime + ' ' + chkAmPm, "%I:%M %p")  #:(inpStartTime + ' ' + chkAmPm)
        if startTime:
            return {'status': 'ok', 'message': 'inpStartTime was valid', 'value' : startTime.strftime('%I:%M %p')}
        else:
            return {'status': 'error', 'message': 'Start time format was not valid', 'value' : inpStartTime}
    else:
        return {'status': 'error', 'message': 'Start time is a required field', 'value' : inpStartTime}

# ---------------------------------------------------------------------------------------------------
def validateClassDuration(inpClassDuration):
    if not inpClassDuration:
        return {'status': 'error', 'message': 'Class duration is a required field', 'value' : inpClassDuration}
    if not str(inpClassDuration).isdigit():
        return {'status': 'error', 'message': 'Class duration must be an integer value between 30 and 120', 'value' : inpClassDuration}
    if int(inpClassDuration) < 30 or int(inpClassDuration) > 120:
        return {'status': 'error', 'message': 'Class duration must be an integer value between 30 and 120', 'value' : inpClassDuration}
    return {'status': 'ok', 'message': 'Class duration was valid', 'value' : inpClassDuration}

# ---------------------------------------------------------------------------------------------------
def calculateFinisTime(chkAmPm, vldStartTime, vldClassDuration):
    if vldStartTime['status'] == 'error' or vldClassDuration['status'] == 'error':
        return {'status': 'err', 'message': 'Could not calculate class end time'}
    inpStartTime      = vldStartTime['value']
    inpClassDuration  = vldClassDuration['value']
    #date_string     = "01-Jan-1900 " + inpStartTime.strftime('%I:%M') + " " + chkAmPm
    date_string     = "01-Jan-1900 " + inpStartTime
    tempDateTime    = datetime.strptime(date_string, "%d-%b-%Y %I:%M %p")
    minutesToAdd    = timedelta(minutes=int(inpClassDuration))
    tempNewDateTime = tempDateTime + minutesToAdd
    return {'status': 'ok', 'message': 'Class duration was valid', 'value' : tempNewDateTime.strftime("%I:%M %p").lstrip('0')}

# ---------------------------------------------------------------------------------------------------
def validate_time_format(time_string, time_format):
    try:
        return datetime.strptime(time_string, time_format)
    except ValueError:
        return False

# 00 = {dict: 2} {'name': 'inpClassName', 'value': 'Chanbara Youth (4 to 10 years of age) '}
# 01 = {dict: 2} {'name': 'slctStyleNum', 'value': '2'}
# 02 = {dict: 2} {'name': 'slctDayOfWeek', 'value': '1'}
# 03 = {dict: 2} {'name': 'inpStartTime', 'value': '5:00 PM'}
# 04 = {dict: 2} {'name': 'inpClassDuration', 'value': '50'}
# 05 = {dict: 2} {'name': 'chkWhite', 'value': 'on'}
# 06 = {dict: 2} {'name': 'chkOrange', 'value': 'on'}
# 07 = {dict: 2} {'name': 'chkYellow', 'value': 'on'}
# 08 = {dict: 2} {'name': 'chkBlue', 'value': 'on'}
# 09 = {dict: 2} {'name': 'chkGreen', 'value': 'on'}
# 10 = {dict: 2} {'name': 'chkPurple', 'value': 'on'}
# 11 = {dict: 2} {'name': 'chkBrown', 'value': 'on'}
# 12 = {dict: 2} {'name': 'chkBlack', 'value': 'on'}
# 13 = {dict: 2} {'name': 'inpAllowedAges', 'value': ''}