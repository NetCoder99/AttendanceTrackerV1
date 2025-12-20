# ---------------------------------------------------------------------------------------------------
import re

import phonenumbers


def validateStudentFieldsUpdate(classData):
    validationResults = {}

    validationResults['frmFirstName']  = validateStudentFirstName(classData['frmFirstName'])
    validationResults['frmLastName']   = validateStudentLastName(classData['frmLastName'])
    validationResults['frmPhoneHome']  = validatePhoneNumberHome(classData['frmPhoneHome'])


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
        return {'status' : 'ok','message': 'inpStudentFirstName was valid'}
    else:
        return {'status' : 'error','message': 'Student first name is a required field'}

# ---------------------------------------------------------------------------------------------------
def validateStudentLastName(inpStudentLastName):
    if inpStudentLastName:
        return {'status' : 'ok','message': 'inpStudentLastName was valid'}
    else:
        return {'status' : 'error','message': 'Student last name is a required field'}

# ---------------------------------------------------------------------------------------------------
def validatePhoneNumberHome(frmPhoneHome):
    if frmPhoneHome:
        try:
            pattern = re.compile(r"^\(?\d{3}\)?[ -]?\d{3}[ -]?\d{4}$")
            if pattern.match(frmPhoneHome):
                return {'status' : 'ok','message': 'frmPhoneHome was valid' }
            else:
                return {'status' : 'error','message': 'Home phone number is invalid'}
        except Exception as ex:
            return {'status': 'error', 'message': 'Home phone number is invalid'}
    else:
        return {'status': 'ok', 'message': 'frmPhoneHome was valid'}
