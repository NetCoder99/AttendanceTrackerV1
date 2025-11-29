import json
import copy

from flask import Blueprint, render_template, request, jsonify

from sqlite.sqlite_students import GetSqliteStudents, UpdStudentPictureStmt, UpdStudentPicture

# Defining a blueprint
students_bp = Blueprint(
    'students_bp', __name__,
    template_folder='templates',
    static_folder='static'
)

@students_bp.route('/students')   # Focus here
def students_bp_home():
    student_records = GetSqliteStudents()
    return render_template('students_list.html', student_records=student_records)

@students_bp.route('/student_search', methods=['POST'])   # Focus here
def students_bp_search():
    if request.method == 'POST':
        data = request.get_json()
        student_records = GetSqliteStudents()
        search_records = copy.deepcopy(student_records)
        if data['searchBadgeNumber']:
            search_records = [x for x in search_records if
                              str(x['badgeNumber']).lower() == str(data['searchBadgeNumber'].lower())]
        else:
            if data['searchFirstName']:
                search_records = [x for x in search_records if
                                  x['firstName'].lower().startswith(data['searchFirstName'].lower())]
            if data['searchLastName']:
                search_records = [x for x in search_records if
                                  x['lastName'].lower().startswith(data['searchLastName'].lower())]
        return search_records

@students_bp.route('/students_details')   # Focus here
def students_bp_details():
    badgeNumber = request.args['badgeNumber']
    student_records = GetSqliteStudents()
    student_record = [x for x in student_records if
                      str(x['badgeNumber']).lower() == badgeNumber.lower()][0]
    student_record['headerMessage'] = 'Updating a student record.'
    return render_template('student_details.html', studentFields=student_record)

@students_bp.route('/save_student_picture', methods=['POST'])
def save_student_picture():
    data_bytes = request.data
    data_string = data_bytes.decode('utf-8')
    data_json = json.loads(data_string)
    # save updated picture to database
    updateStmt = UpdStudentPicture(data_json)
    returnData = data_json['fileBase64']
    return str(data_json['fileBase64'])

