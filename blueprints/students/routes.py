import json
from dateutil.parser import parse, ParserError
from datetime import date, datetime

from flask import Blueprint, render_template, request, jsonify
from flask_htmx import make_response
from sqlalchemy import select, func

import constants
from blueprints.belts.sqlite_belts import GetBeltsRecords, GetStripeRecords, GetRanksRecords, GetStripesForRankStmt
from blueprints.students.student_attendance import UpdPromotionDateStmt, InsertAttendanceRecord, GetAttendanceRecord
from blueprints.students.student_promotions import GetNextPromotion
from blueprints.students.validate_student_fields import validateStudentFieldsUpdate
from models import Classes, Students, Attendance, Promotions
from services.barcodeGenerator import createBarcodeFile
from services.battoDoGenerator import createBattoDoBadgePdf
from services.checkin_procs import GetCurrentClass
from services.list_procs import FormListToDict
from blueprints.students.sqlite_students import *
from services.pdfGenerator import createBadgePdf
from sqlite.sqlite_alchemy import getDbSession
from sqlite.sqlite_procs import GetDataWithArgs, UpdDataWithArgs, GetDataNoArgs

db_session = getDbSession()

# Defining a blueprint
students_bp = Blueprint(
    'students_bp', __name__,
    template_folder='templates',
    static_folder='static',
    static_url_path='/students_bp_static'
)

@students_bp.route('/students')   # Focus here
def students_bp_home():
    print(f'Current route: students_bp_home')
    student_records = GetSqliteStudents()
    return render_template('students_main.html', student_records=student_records)

@students_bp.route('/get_student_details', methods=['GET', 'POST'])   # Focus here
def get_student_details():
    print(f'Current route: get_student_details')
    try:
        badgeNumber     = request.json['badgeNumber']
        sqlQueryStudent = GetStudentRecordsStmtByBadge()
        student_records = GetDataWithArgs(sqlQueryStudent, {'badgeNumber' : badgeNumber})
        if len(student_records) != 1:
            raise Exception("Invalid student record count.")
        return student_records[0]
    except Exception as ex:
        print(f'Error: {ex.__str__()}')

@students_bp.route('/student_create', methods=['GET', 'POST'])
def student_create():
    print(f'Current route: student_create')
    try:
        imageData   = GetDataWithArgs(GetDefaultImageStmt(), {'imageName' : 'RSM_Logo2.webp'})[0]
        student_record = {'':''}
        return render_template('student_create.html', studentFields=student_record)
    except Exception as ex:
        print(f'Error: {ex.__str__()}')

@students_bp.route('/student_list_api', methods=['GET', 'POST'])
def student_list_api():
    print(f'Current route: student_list_api')
    try:
        student_records = GetSqliteStudents()
        return json.dumps(student_records)
    except Exception as ex:
        print(f'Error: {ex.__str__()}')

@students_bp.route('/student_details_api', methods=['GET', 'POST'])
def students_details_api():
    print(f'Current route: students_details_api')
    try:
        badgeNumber     = request.json['badgeNumber']
        student_records = GetSqliteStudents()
        student_record  = [x for x in student_records if
                          str(x['badgeNumber']).lower() == badgeNumber.lower()][0]
        return json.dumps(student_record)
    except Exception as ex:
        print(f'Error: {ex.__str__()}')

@students_bp.route('/student_create_api', methods=['GET', 'POST'])
def student_create_api():
    print(f'Current route: student_create_api')
    try:
        student_record  = GetDataNoArgs(GetDefaultStudentDataStmt())[0]
        return json.dumps(student_record)
    except Exception as ex:
        print(f'Error: {ex.__str__()}')

@students_bp.route('/save_student_picture', methods=['POST'])
def save_student_picture():
    try:
        print(f'Current route: save_student_picture')
        data_bytes  = request.data
        data_string = data_bytes.decode('utf-8')
        data_json   = json.loads(data_string)
        pattern = re.compile(r"^(data):(image)/(.*);(base64),(.+)")
        matches = pattern.search(data_json['fileBase64'])
        updateDict  = {
            'badgeNumber' : data_json['badgeNumber'],
            'studentImageName' : data_json['file_name'],
            'studentImageType' : matches.group(3),
            'studentImageBase64' : matches.group(5),
            'fileBase64' :  data_json['fileBase64']
        }
        UpdStudentPicture(data_json, updateDict)
        return json.dumps(updateDict)
    except Exception as ex:
        print(f'Error: {ex.__str__()}')
        return json.dumps({"error" : ex.__str__()})

# @students_bp.route('/student_promotions')   # Focus here
# def student_promotions():
#     print(f'Current route: student_promotions')
#     try:
#         badgeNumber     = request.args['badgeNumber']
#         studentData     = GetDataWithArgs(GetStudentRecordsStmtByBadge(), {'badgeNumber': request.args['badgeNumber']})
#         belt_records    = GetBeltsRecords()
#
#         stripe_records  = GetStripeRecords({'rankNum': '1'})
#         #student_record['headerMessage'] = 'Reviewing student promotions.'
#
#         return render_template('student_promotions.html', studentFields=studentData)
#
#
#     except Exception as ex:
#         print(f'Error: {ex.__str__()}')

@students_bp.route('/student_attendance', methods=['GET', 'POST'])   # Focus here
def student_attendance():
    try:
        badgeNumber = request.args['badgeNumber']
        student_records = GetSqliteStudents()
        student_record = [x for x in student_records if
                          str(x['badgeNumber']).lower() == badgeNumber.lower()][0]
        student_record['headerMessage'] = 'Reviewing student attendance.'
        return render_template('student_attendance.html', studentFields=student_record)
    except Exception as ex:
        print(f'Error: {ex.__str__()}')

@students_bp.route('/student_attendance_api', methods=['GET', 'POST'])   # Focus here
def student_attendance_api():
    try:
        badgeNumber     = request.json['badgeNumber']
        sqlQueryStudent = GetStudentRecordsStmtByBadge()
        studentData     = GetDataWithArgs(sqlQueryStudent, {'badgeNumber' : badgeNumber})

        sqlQueryAttendance = GetStudentAttendanceRecords()
        attendanceData     = GetDataWithArgs(sqlQueryAttendance, {'badgeNumber' : badgeNumber})

        attendance_total_count = (db_session
                                      .scalar(select(func.count(Attendance.badgeNumber))
                                      .where(Attendance.badgeNumber == badgeNumber))
                                      )
        last_promotion_date = (db_session
                                      .scalar(select(func.max(Promotions.promotionDate))
                                      .where(Promotions.badgeNumber == badgeNumber))
                                      )
        last_promotion_date_str = parse(last_promotion_date, fuzzy=False).strftime(constants.fmtDate)
        next_promotion_data     = GetNextPromotion(badgeNumber)

        rtnData = {
            'studentData'            : studentData[0],
            'attendanceData'         : attendanceData,
            'attendance_total_count' : attendance_total_count,
            'last_promotion_date'    : last_promotion_date_str,
            'next_belt_name'         : next_promotion_data['beltTitle'],
            'next_stripe_title'      : next_promotion_data['stripeTitle']
        }
        return rtnData
    except Exception as ex:
        print(f'Error: {ex.__str__()}')


@students_bp.route('/save_student_details_api', methods=['GET', 'POST'])
def save_student_details_api():
    print(f'Current route: save_student_details_api')
    form_dict  = FormListToDict(request.json)
    validation_results = validateStudentFieldsUpdate(form_dict)
    if validation_results['validationResults']['status'] == 'ok':
        badgeNumber     = form_dict['badgeNumber']
        sqlQueryStudent = GetStudentRecordsStmtByBadge()
        studentData     = GetDataWithArgs(sqlQueryStudent, {'badgeNumber' : badgeNumber})
        if len(studentData) == 0:
            InsStudentRecord(form_dict)
            SetInitialRank(badgeNumber)
        else:
            UpdStudentRecord(form_dict)
    return validation_results

def SetInitialRank(badgeNumber):
    beltData          = GetRanksRecords()
    stripeData        = GetDataWithArgs(GetStripesForRankStmt(), {'rankNum' : 1})
    whiteBelt         = [x for x in beltData if x['rankNum'] == 1][0]
    whiteStripe       = stripeData[0]

    updStudentDict    = {
        'currentRankNum'    : whiteBelt['rankNum'],
        'currentRankName'   : whiteBelt['rankName'],
        'currentStripeId'   : whiteStripe['stripeId'],
        'currentStripeName' : whiteStripe['stripeName'],
        'badgeNumber'       : badgeNumber,
        # 'studentPromotionDate': request.json['promotionDate']
    }

    # adjust the date to consistent format
    studentPromotionDate = datetime.now().strftime(constants.fmtDateTime)
    updStudentDict['studentPromotionDate'] = studentPromotionDate
    updStudentDict['comments'] = 'Initial Rank'

    # update the student record
    updStudentQuery   = UpdateStudentRankStmt()
    updateCounts      = UpdDataWithArgs(updStudentQuery, updStudentDict)

    #insert the history record
    insertPromotionStmt = InsertPromotionsRankStmt()
    studentData         = GetDataWithArgs(GetStudentRecordsStmtByBadge(), {'badgeNumber': badgeNumber})
    insertPromotionDict = GetInsertPromotionDict(studentData, updStudentDict)
    insertCounts        = UpdDataWithArgs(insertPromotionStmt, insertPromotionDict)

@students_bp.route('/create_badge_api', methods=['GET', 'POST'])
def create_badge_api():
    try:
        print(f'Current route: create_badge_api')
        badgeNumber   = request.json['badgeNumber']
        sqlQuery      = GetStudentRecordsStmtByBadge()
        studentData   = GetDataWithArgs(sqlQuery, {'badgeNumber' : badgeNumber})
        createBarcodeFile(badgeNumber)
        createBadgePdf(badgeNumber, studentData[0])
        return {"status" : 'ok'}
    except Exception as ex:
        print(f'Error: {ex.__str__()}')

@students_bp.route('/create_batto_do_badge_api', methods=['GET', 'POST'])
def create_batto_do_badge_api():
    try:
        print(f'Current route: create_batto_do_badge_api')
        badgeNumber   = request.json['badgeNumber']
        sqlQuery      = GetStudentRecordsStmtByBadge()
        studentData   = GetDataWithArgs(sqlQuery, {'badgeNumber' : badgeNumber})
        createBarcodeFile(badgeNumber)
        createBattoDoBadgePdf(badgeNumber, studentData[0])
        #createBadgePdf(badgeNumber, studentData[0])
        return {"status" : 'ok'}
    except Exception as ex:
        print(f'Error: {ex.__str__()}')

@students_bp.route('/get_stripe_names', methods=['GET', 'POST'])
def get_stripe_names():
    print(f'Current route: get_stripe_names')
    sqlQuery      = GetStripeNamesByRank()
    stripeRecords = GetDataWithArgs(sqlQuery, request.json)
    return stripeRecords

@students_bp.route('/upd_student_rank', methods=['GET', 'POST'])
def upd_student_rank():
    print(f'Current route: upd_student_rank')
    studentData       = GetDataWithArgs(GetStudentRecordsStmtByBadge(), {'badgeNumber': request.json['badgeNumber']})
    promotionHistory  = GetDataWithArgs(GetPromotionHistoryStmt(), request.json)

    # do not apply if no changes
    if IsDuplicatePromotion(studentData, request.json):
        return {'status': 'error', 'badgeNumber': request.json['badgeNumber'],
                'message': 'Current promotion matches last promotion!'}

    updStudentQuery   = UpdateStudentRankStmt()
    updStudentDict    = {
        'currentRankNum'    : request.json['beltId'],
        'currentRankName'   : request.json['beltTitle'],
        'currentStripeId'   : request.json['stripeId'],
        'currentStripeName' : request.json['stripeTitle'],
        'badgeNumber'       : request.json['badgeNumber'],
        # 'studentPromotionDate': request.json['promotionDate']
    }

    # adjust the date to consistent format
    studentPromotionDate = parse(request.json['promotionDate'], fuzzy=False).strftime(constants.fmtDateTime)
    updStudentDict['studentPromotionDate'] = studentPromotionDate
    updStudentDict['comments'] = 'Promotion'

    # update the student record
    updateCounts = UpdDataWithArgs(updStudentQuery, updStudentDict)

    #insert the history record
    insertPromotionStmt = InsertPromotionsRankStmt()
    insertPromotionDict = GetInsertPromotionDict(studentData, updStudentDict)
    insertCounts        = UpdDataWithArgs(insertPromotionStmt, insertPromotionDict)

    return {'status': 'ok',
            'badgeNumber': request.json['badgeNumber'],
            'lastRowId': updateCounts['lastrowid'],
            'rowCount': updateCounts['rowcount']
            }


def GetInsertPromotionDict(studentData: dict, updStudentDict: dict):
    return {
        'badgeNumber': studentData[0]['badgeNumber'],
        'beltId':      updStudentDict['currentRankNum'],
        'beltTitle':   updStudentDict['currentRankName'],
        'stripeId':    updStudentDict['currentStripeId'],
        'stripeTitle': updStudentDict['currentStripeName'],
        'studentFirstName': studentData[0]['firstName'],
        'studentLastName' : studentData[0]['lastName'],
        'promotionDate'   : updStudentDict['studentPromotionDate'],
        'comments'        : updStudentDict['comments']
    }


def IsDuplicatePromotion(studentData, requestJson) -> bool:
    if studentData[0]['currentRankNum'] is None:
        return False

    currentRankNum   = int(studentData[0]['currentRankNum'])
    selectedBeltId   = int(requestJson['beltId'])
    currentStripeId  = int(studentData[0]['currentStripeId'])
    selectedStripeId = int(requestJson['stripeId'])

    if studentData[0]['studentPromotionDate'] is None:
        currentPromotionDate = datetime.fromisoformat("1900-01-01T00:00:00")
    else:
        currentPromotionDate = parse(studentData[0]['studentPromotionDate'], fuzzy=False).date()

    selectedPromotionDate = parse(request.json['promotionDate'], fuzzy=False).date()

    if (   currentRankNum == selectedBeltId
       and currentStripeId == selectedStripeId
       and currentPromotionDate == selectedPromotionDate):
        return True

    return False

def getPromotionMessage():
    pass

@students_bp.route('/get_promotion_history', methods=['GET', 'POST'])
def get_promotion_history():
    print(f'Current route: get_promotion_history')
    sqlQuery          = GetPromotionHistoryStmt()
    promotionHistory  = GetDataWithArgs(sqlQuery, request.json)
    return promotionHistory

@students_bp.route('/save_promotion_date', methods=['GET', 'POST'])
def save_promotion_date():
    print(f'Current route: save_promotion_date')
    promotionId   = request.form['promotionId']
    promotionDate = parse(request.form['promotionDate'], fuzzy=False).strftime(constants.fmtDateTime)
    updateDate    = datetime.now().strftime(constants.fmtDateTime)
    updateDict    = {
        'promotionDate'  :promotionDate,
        'updateDateTime' :updateDate,
        'promotionId'    :promotionId
    }
    updateCounts = UpdDataWithArgs(UpdPromotionDateStmt(), updateDict)
    return "Promotion date was updated."

@students_bp.route('/get_attendance_dialog', methods=['GET', 'POST'])
def get_attendance_dialog():
    print(f'Current route: get_attendance_dialog')
    if 'hdnBadgeNumber' in request.args:
        badge_number = request.args['hdnBadgeNumber']
    elif  'hdnBadgeNumber' in request.form:
        badge_number = request.form['hdnBadgeNumber']
    if not badge_number:
        raise Exception ("Badge number is required!")

    modal_rank = render_template(
        "partials/new_attendance_form.html", badge_number=badge_number
    )
    response = make_response(modal_rank)
    response.headers['HX-Retarget'] = '#new-attendance-record'
    response.headers['HX-Reswap'] = 'innerHTML'
    response.headers['HX-Trigger-After-Settle'] = 'show_rank_required_dialog'
    return response

# --------------------------------------------------------------------
@students_bp.route('/update_attendance_record', methods=['POST'])
def update_attendance_record():
    try:
        badge_number    = request.form['badge_number']

        # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
        student_record = db_session.query(Students).filter_by(badgeNumber=badge_number).first()
        if not student_record:
            raise Exception("Student record not found!")

        # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
        checkin_datetime = parse(request.form['frm_checkinDateTime'])
        selected_class   = GetCurrentClass(checkin_datetime)
        if not selected_class:
            raise Exception('No class found.')

        day_of_week = checkin_datetime.weekday() + 1
        duplicate_record = GetAttendanceRecord(int(badge_number), checkin_datetime)
        if len(duplicate_record) > 0:
            raise Exception('Duplicate attendance record not inserted!')

        InsertAttendanceRecord(student_record, selected_class, checkin_datetime)

        return getAttendanceUpdateMessage('completed', 'New attendance record was added.')
        #return update_required_rank_func()
    except Exception as ex:
        print(str(ex))
        return getAttendanceUpdateMessage('error', str(ex))

# -------------------------------------------------------
def getAttendanceUpdateMessage(status, message):
    alert_class = "text-danger" if status == 'error' else "text-success"
    html_snippet = f'<h5 id="rank_update_message" class="{alert_class} fw-bold text-center mb-3">{message}</h5>'
    response = make_response(html_snippet)
    response.headers['HX-Trigger'] = f'ranks_response_{status}'  # CSS Selector
    return response

# --------------------------------------------------------------------
@students_bp.route('/get_attendance_class', methods=['GET', 'POST'])
def get_attendance_class():
    validation_results = validate_class_search(request.args)
    if not validation_results[0]:
        status = 'error'
        alert_class = "text-danger" # if status == 'error' else "text-success"
        message = validation_results[1]
        message_snippet = f'<h5 id="rank_update_message" class="{alert_class} fw-bold text-center mb-3">{message}</h5>'
        response = make_response(message_snippet)
        #response.headers['HX-Trigger'] = f'ranks_response_{status}'  # CSS Selector
        return response
    else:
        status       = 'completed'
        alert_class  = "text-danger" if status == 'error' else "text-success"
        message      = "Class search completed"
        class_data   = validation_results[1]
        class_details = render_template(
            "partials/new_attendance_class.html",
            classDayName = "Monday",
            className = class_data.classDisplayTitle,
            classStartTime=class_data.classStartTime,
            classFinisTime=class_data.classFinisTime,
        )
        attendance_message = f"""
                <div id="div_attendance_messages" name="div_attendance_messages" class="mb-3 d-inline-block" hx-oob-swap="true">
                    <h5 id="attendance_update_message" class="text-success fw-bold text-center mb-3">{message}</h5>
                </div>
        """
        return f"{class_details}{attendance_message}"   #response

def validate_class_search(form_args: dict) -> (bool, Classes):
    if len(form_args) == 0:
        return False, "Attendance form had no values!"
    if not str(form_args['frm_checkinDateTime']):
        return False, "Checkin date and time is required!"

    try:
        checkin_date_time = parse(form_args['frm_checkinDateTime'])
        selected_class    = GetCurrentClass(checkin_date_time)
        if not selected_class:
            return False, "No class found for that date and time!"
    except Exception as ex:
        print(f'{str(ex)}')
        return False, str(ex)

    return True, selected_class

# @students_bp.route('/get_student_details', methods=['GET', 'POST'])
# def get_student_details():
#     print(f'Current route: get_student_details')
#     sqlQuery          = GetPromotionHistoryStmt()
#     promotionHistory  = GetDataWithArgs(sqlQuery, request.json)
#     return promotionHistory
