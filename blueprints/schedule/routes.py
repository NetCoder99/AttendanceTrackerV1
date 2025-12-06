import json
import copy

from flask import Blueprint, render_template, request, jsonify

from blueprints.schedule.validateClassFields import validateClassFields
from sqlite.sqlite_schedule import GetClassRecords, GetClassRecordsSorted

schedule_bp = Blueprint(
    'schedule_bp', __name__,
    template_folder='templates',
    static_folder='static',
    static_url_path='/schedule_bp_static'
)

@schedule_bp.route('/schedule')
def schedule_bp_home():
    #class_records = GetClassRecordsSorted()
    return render_template('schedule_list.html')

@schedule_bp.route('/schedule_api', methods=['POST', 'GET'])
def schedule_api():
    class_records = GetClassRecordsSorted()
    return jsonify({"data": class_records})

@schedule_bp.route('/getClassDetails_api', methods=['POST', 'GET'])
def classDetails_api():
    classNum       = request.json['classNum']
    class_records = GetClassRecordsSorted()
    if classNum:
        class_record = [x for x in class_records if str(x['classNum']) == str(classNum)]
        return {"data": class_record[0]}

    return None

@schedule_bp.route('/saveClassDetails_api', methods=['POST', 'GET'])
def saveClassDetails_api():
    isValid    = validateClassFields(request.json)
    return jsonify(isValid)

@schedule_bp.route('/deleteClassDetails_api', methods=['POST', 'GET'])
def deleteClassDetails_api():
    isValid    = validateClassFields(request.json)
    return jsonify(isValid)
