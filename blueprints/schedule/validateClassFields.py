from datetime import datetime, date, time, timedelta

import json
from time import strptime, strftime


def validateClassFields(classData):
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
            return {'status': 'ok', 'message': 'inpStartTime was valid', 'value' : startTime}
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
    date_string     = "01-Jan-1900 " + inpStartTime.strftime('%I:%M') + " " + chkAmPm
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