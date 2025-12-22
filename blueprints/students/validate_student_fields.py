# ---------------------------------------------------------------------------------------------------
from datetime import datetime
import re

import phonenumbers

from sqlite.sqlite_common import GetStateCodesStmt, GetZipCodesStmt
from sqlite.sqlite_procs import GetDataNoArgs, GetDataWithArgs


def validateStudentFieldsUpdate(classData):
    validationResults = {}

    validationResults['frmFirstName'] = validateStudentFirstName(classData['frmFirstName'])
    validationResults['frmLastName'] = validateStudentLastName(classData['frmLastName'])
    validationResults['frmPhoneHome'] = validatePhoneNumberHome(classData['frmPhoneHome'])
    validationResults['frmState'] = validateStudentState(classData['frmState'])
    validationResults['frmZip'] = validateStudentZipCode(classData['frmZip'])
    validationResults['frmBirthDate'] = validateStudentBirthDate(classData['frmBirthDate'])
    validationResults['frmEmail'] = validateStudentEmail(classData['frmEmail'])

    # '''
    # 	Line  20:                                 <input id="selectStudentPicture" style="display:none;" type="file">
    # 	Line  55:                                 <input id="frmFirstName"
    # 	Line  65:                                 <input id="frmMiddleName"
    # 	Line  76:                                 <input id="frmLastName"
    # 	Line  88:                                 <input id="frmAddress"
    # 	Line 100:                                 <input id="frmAddress2"
    # 	Line 113:                                 <input id="frmCity"
    # 	Line 126:                                 <input id="frmState"
    # 	Line 136:                                 <input id="frmZip"
    # 	Line 146:                                 <input id="frmBirthDate"
    # 	Line 159:                                 <input id="frmPhoneHome"
    # 	Line 169:                                 <input id="frmEmail"
    # 	Line 193:                             <div id="divStudentMessages" class="fw-bold text-success">Awaiting input ...</div>
    # '''

    # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    errCount = len({k: v for k, v in validationResults.items() if v['status'] == 'error'})
    if errCount == 0:
        validationResults['validationResults'] = {'status': 'ok', 'message': 'Class changes have been saved'}
    else:
        validationResults['validationResults'] = {'status': 'error', 'message': f'Validation error count : {errCount}'}
    return validationResults


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
def validateStudentState(frmState):
    if not frmState:
        return {'status': 'ok', 'message': 'Student state was not entered'}
    pattern = re.compile(r"^[a-zA-Z]{2}$")
    if not pattern.match(frmState):
        return {'status': 'error', 'message': 'State code must be 2 characters'}
    frmState = frmState.upper()
    stateCodesStmt = GetStateCodesStmt()
    stateCodes = GetDataNoArgs(stateCodesStmt)
    foundEntry = [z for z in stateCodes if z['physicalState'] == frmState]
    if len(foundEntry) == 0:
        return {'status': 'error', 'message': 'State code was not found'}
    return {'status': 'ok', 'message': 'Student state code was valid'}

# ---------------------------------------------------------------------------------------------------
def validateStudentZipCode(frmZip):
    if not frmZip:
        return {'status': 'ok', 'message': 'Student zipcode was not entered'}
    pattern = re.compile(r"^[0-9]{5}$")
    if not pattern.match(frmZip):
        return {'status': 'error', 'message': 'Student zip code must be 5 digits'}
    stateCodesStmt = GetZipCodesStmt()
    zipCodes = GetDataWithArgs(stateCodesStmt, {'physicalZip' : frmZip})
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
