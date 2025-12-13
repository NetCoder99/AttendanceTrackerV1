# ---------------------------------------------------------------------------------------------------
def validateStudentFieldsUpdate(classData):
    validationResults = {}
    validationResults['validationStudentResults'] = {'status': 'ok', 'message': 'Student changes have been saved'}

# '''
# form_dict = {dict: 10} {'frmAddress': '14213 N. BRUNSWICK DR', 'frmAddress2': 'APT A', 'frmBirthDate': '', 'frmCity': 'Fountain Hills', 'frmEmail': '', 'frmFirstName': 'Jennifer', 'frmLastName': 'Hesterman', 'frmPhoneHome': '480-304-0327', 'frmState': 'AZ', 'frmZip': '85268'}
#  'frmFirstName' = {str} 'Jennifer'
#  'frmLastName' = {str} 'Hesterman'
#  'frmAddress' = {str} '14213 N. BRUNSWICK DR'
#  'frmAddress2' = {str} 'APT A'
#  'frmCity' = {str} 'Fountain Hills'
#  'frmState' = {str} 'AZ'
#  'frmZip' = {str} '85268'
#  'frmPhoneHome' = {str} '480-304-0327'
#  'frmEmail' = {str} ''
#  'frmBirthDate' = {str} ''
#  __len__ = {int} 10
#  '''

    # # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    # validationResults['inpClassName'] = validateClassName(inpClassName)
    # # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    # errCount = len({k: v for k, v in validationResults.items() if v['status'] == 'error'})
    # if errCount == 0:
    #     validationResults['validationResults'] = {'status': 'ok', 'message': 'Class changes have been saved'}
    # else:
    #     validationResults['validationResults'] = {'status': 'error', 'message': f'Validation error count{errCount}'}
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