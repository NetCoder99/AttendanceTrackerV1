import json
import copy

from flask import Blueprint, render_template, request, jsonify

from blueprints.schedule.validateClassFields import validateClassFieldsUpdate, getSqlClassInsertDict, \
    validateClassFieldsInsert, getSqlClassUpdateDict
from sqlite.sqlite_schedule import GetClassRecords, GetClassRecordsSorted, DeleteClass, InsertNewClass, \
    UpdateExistingClass

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
def getClassDetails_api():
    classNum       = request.json['classNum']
    class_records = GetClassRecordsSorted()
    if classNum:
        class_record = [x for x in class_records if str(x['classNum']) == str(classNum)]
        return {"data": class_record[0]}

    return None

@schedule_bp.route('/saveClassDetails_api', methods=['POST', 'GET'])
def saveClassDetails_api():
    classData = request.json
    classNumEntry = [x for x in classData if x['name'] == 'classNum'][0]

    if classNumEntry['value']:
        validationResults = validateClassFieldsUpdate(classData)
        if validationResults['validationResults']['status'] == 'ok':
            print(f'Updating class details')
            classDict = getSqlClassUpdateDict(classData)
            UpdateExistingClass(classDict)
    else:
        validationResults = validateClassFieldsInsert(classData)
        if validationResults['validationResults']['status'] == 'ok':
            vldStartTime     = validationResults['inpStartTime']
            vldClassDuration = validationResults['inpClassDuration']
            vldFinisTime     = validationResults['inpFinisTime']
            classDict = getSqlClassInsertDict(request.json, vldStartTime, vldClassDuration, vldFinisTime)
            InsertNewClass(classDict)

    return jsonify(validationResults)

@schedule_bp.route('/deleteClassDetails_api', methods=['POST', 'GET'])
def deleteClassDetails_api():
    delCount = DeleteClass(request.json)
    result = {'status': 'ok', 'message': f'{delCount} class has been deleted'}
    return jsonify(result)
