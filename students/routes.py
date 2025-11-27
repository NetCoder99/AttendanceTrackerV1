import json
import copy

from flask import Blueprint, render_template, request, jsonify

from sqlite.sqlite_students import GetSqliteStudents

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
