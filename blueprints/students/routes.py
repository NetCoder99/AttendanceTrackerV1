import json
import os
import re

import barcode
from barcode.writer import ImageWriter
from flask import Blueprint, render_template, request

from blueprints.students.validate_student_fields import validateStudentFieldsUpdate
from services.barcodeGenerator import createBarcodeFile
from services.list_procs import FormListToDict
from blueprints.students.sqlite_students import GetSqliteStudents, UpdStudentPicture, UpdStudentRecord, \
    GetStudentRecordsStmtByBadge
from services.pdfGenerator import createBadgePdf
from sqlite.sqlite_procs import GetDataWithArgs

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

@students_bp.route('/student_details', methods=['GET', 'POST'])   # Focus here
def students_bp_details():
    print(f'Current route: students_bp_details')
    try:
        badgeNumber     = request.json['badgeNumber']
        student_records = GetSqliteStudents()
        student_record  = [x for x in student_records if
                          str(x['badgeNumber']).lower() == badgeNumber.lower()][0]
        student_record['headerMessage'] = 'Updating a student record.'
        return render_template('student_details.html', studentFields=student_record)
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

@students_bp.route('/student_promotions')   # Focus here
def student_promotions():
    try:
        badgeNumber = request.args['badgeNumber']
        student_records = GetSqliteStudents()
        student_record = [x for x in student_records if
                          str(x['badgeNumber']).lower() == badgeNumber.lower()][0]
        student_record['headerMessage'] = 'Reviewing student promotions.'
        return render_template('student_promotions.html', studentFields=student_record)
    except Exception as ex:
        print(f'Error: {ex.__str__()}')

@students_bp.route('/student_attendance')   # Focus here
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

@students_bp.route('/save_student_details_api', methods=['GET', 'POST'])
def save_student_details_api():
    print(f'Current route: save_student_details_api')
    #data_bytes = request.data
    form_dict  = FormListToDict(request.json)
    validation_results = validateStudentFieldsUpdate(form_dict)
    if validation_results['validationResults']['status'] == 'ok':
        UpdStudentRecord(form_dict)
    return validation_results

@students_bp.route('/create_badge_api', methods=['GET', 'POST'])
def create_badge_api():
    print(f'Current route: create_badge_api')
    badgeNumber   = request.json['badgeNumber']
    sqlQuery      = GetStudentRecordsStmtByBadge()
    studentData   = GetDataWithArgs(sqlQuery, {'badgeNumber' : badgeNumber})
    createBarcodeFile(badgeNumber)
    createBadgePdf(badgeNumber, studentData[0])
    return {"status" : 'ok'}
