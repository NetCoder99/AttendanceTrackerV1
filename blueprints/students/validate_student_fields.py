# ---------------------------------------------------------------------------------------------------
import re
import logging.config
from sqlalchemy import select, func
from datetime import datetime

from models.data_models import Students
from sqlite.sqlite_alchemy import getDbSession
from sqlite.sqlite_common import GetStateCodesStmt, GetZipCodesStmt
from sqlite.sqlite_procs import GetDataNoArgs, GetDataWithArgs

logger = logging.getLogger(__name__)
db_session = getDbSession()

def getFirstValidationError(validationResults: dict) -> dict | None:
    for validationResult in validationResults:
        if validationResults[validationResult]['status'] == 'error':
            return validationResults[validationResult]
    return None

def getErrorFields(validationResults: dict) -> list:
    rtn_list = []
    for validationResult in validationResults:
        if validationResults[validationResult]['status'] == 'error':
            rtn_list.append(validationResult)
    return rtn_list

def validateStudentFieldsUpdate(classData):
    try:
        validationResults = {}
        validationResults['frmField1'] = validateStudentFirstName(classData['frmField1'])
        validationResults['frmField3'] = validateStudentLastName(classData['frmField3'])
        validationResults['frmPhoneHome'] = validatePhoneNumberHome(classData['frmPhoneHome'])
        validationResults['frmField10'] = validateStudentState(classData['frmField10'])
        validationResults['frmField11'] = validateStudentZipCode(classData['frmField11'])
        validationResults['frmBirthDate'] = validateStudentBirthDate(classData['frmBirthDate'])
        validationResults['frmEmail'] = validateStudentEmail(classData['frmEmail'])

        # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
        errCount = len({k: v for k, v in validationResults.items() if v['status'] == 'error'})
        if errCount == 0:
            validationResults['validationResults'] = {'status': 'ok', 'message': 'Class changes have been saved'}
        else:
            validationResults['validationResults'] = {'status': 'error', 'message': f'Validation error count : {errCount}'}
        return validationResults
    except Exception as ex:
        print(f'Error: {ex.__str__()}')
        return {'status': 'error', 'message': ex.__str__()}


# ---------------------------------------------------------------------------------------------------
def validateStudentFirstName(inpStudentFirstName):
    if inpStudentFirstName:
        return {'status': 'ok', 'message': 'inpStudentFirstName was valid'}
    else:
        return {'status': 'error', 'message': 'Student first name is a required field'}


# ---------------------------------------------------------------------------------------------------
def validateStudentLastName(inpStudentLastName):
    if inpStudentLastName:
        return {'status': 'ok', 'message': 'inpStudentLastName was valid'}
    else:
        return {'status': 'error', 'message': 'Student last name is a required field'}


# ---------------------------------------------------------------------------------------------------
def validatePhoneNumberHome(frmPhoneHome):
    if frmPhoneHome:
        try:
            pattern = re.compile(r"^\(?(\d{3})\)?[ -]?(\d{3})[ -]?(\d{4})$")
            if pattern.match(frmPhoneHome):
                match = re.search(pattern, frmPhoneHome)
                rtnPhoneHome = f'{match.group(1)}-{match.group(2)}-{match.group(3)}'
                return {'status': 'ok', 'message': 'Home phone number was valid', 'rtnPhoneHome': rtnPhoneHome}
            else:
                return {'status': 'error', 'message': 'Home phone number is invalid'}
        except Exception as ex:
            print(f'Error: {ex.__str__()}')
            return {'status': 'abend', 'message': ex.__str__()}
    else:
        return {'status': 'ok', 'message': 'frmPhoneHome was valid'}


# ---------------------------------------------------------------------------------------------------
def validateStudentState(frmField10):
    if not frmField10:
        return {'status': 'ok', 'message': 'Student state was not entered'}
    pattern = re.compile(r"^[a-zA-Z]{2}$")
    if not pattern.match(frmField10):
        return {'status': 'error', 'message': 'State code must be 2 characters'}
    frmField10 = frmField10.upper()
    stateCodesStmt = GetStateCodesStmt()

    stateCodes = GetDataNoArgs(stateCodesStmt)
    if not stateCodes:
        return {'status': 'error', 'message': 'State code was not found'}

    foundEntry = [z for z in stateCodes if z['physicalState'] == frmField10]
    if len(foundEntry) == 0:
        return {'status': 'error', 'message': 'State code was not found'}

    return {'status': 'ok', 'message': 'Student state code was valid'}

# ---------------------------------------------------------------------------------------------------
def validateStudentZipCode(frmField11):
    if not frmField11:
        return {'status': 'ok', 'message': 'Student zipcode was not entered'}
    pattern = re.compile(r"^[0-9]{5}$")
    if not pattern.match(frmField11):
        return {'status': 'error', 'message': 'Student zip code must be 5 digits'}
    stateCodesStmt = GetZipCodesStmt()
    zipCodes = GetDataWithArgs(stateCodesStmt, {'physicalZip' : frmField11})

    if not zipCodes:
        return {'status': 'error', 'message': 'State code was not found'}

    if len(zipCodes) == 0:
        return {'status': 'error', 'message': 'Student zip code was not found'}
    return {'status': 'ok', 'message': 'Student zip code was valid'}

def validateStudentBirthDate(frmBirthDate):
    if not frmBirthDate:
        return {'status': 'ok', 'message': 'Student birth date was not entered'}
    patternBirthDate = re.compile(r"^(0[1-9]|1[0-2])[\/\-.](0[1-9]|[12][0-9]|3[01])[\/\-.]\d{4}$")
    if not patternBirthDate.match(frmBirthDate):
        return {'status': 'error', 'message': 'Student birth date must be mm/dd/yyyy'}
    try:
        tempBirthDate = datetime.strptime(frmBirthDate, "%m/%d/%Y")
        return {'status': 'ok', 'message': 'Student birth date was valid'}
    except Exception as ex:
        print(f'Error: {ex.__str__()}')
        return {'status': 'error', 'message': 'Student birth date was not valid'}

def validateStudentEmail(frmEmail):
    if not frmEmail:
        return {'status': 'ok', 'message': 'Student email was not entered'}
    regex_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    if re.fullmatch(regex_pattern, frmEmail):
        return {'status': 'ok', 'message': 'Student email was valid'}
    else:
        return {'status': 'error', 'message': 'Student email was not valid'}

def isDuplicateStudentByName(first_name, last_name) -> bool:
    duplicate_student_stmt = (select(func.count())
        .select_from(Students)
        .where(
            func.lower(Students.firstName) == first_name.lower(),
            func.lower(Students.lastName) == last_name.lower(),
        )
    )
    duplicate_student_count = db_session.scalar(duplicate_student_stmt)
    if duplicate_student_count > 0:
        return True
    else:
        return False
