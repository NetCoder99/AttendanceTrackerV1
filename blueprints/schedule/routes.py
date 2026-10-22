import json
import copy
import logging.config

from flask import Blueprint, render_template, request, jsonify
from sqlalchemy import Float, cast, select

from blueprints.schedule.validate_class_fields import validateClassFieldsUpdate, getSqlClassInsertDict, \
    validateClassFieldsInsert, getSqlClassUpdateDict
from models.data_models import Classes, Schools
from services.schedulePrinter import PrintClassSchedule
from sqlite.sqlite_alchemy import getDbSession
from sqlite.sqlite_schedule import GetClassRecords, GetClassRecordsSorted, DeleteClass, InsertNewClass, \
    UpdateExistingClass

schedule_bp = Blueprint(
    'schedule_bp', __name__,
    template_folder='templates',
    static_folder='static',
    static_url_path='/schedule_bp_static'
)

logger = logging.getLogger(__name__)
db_session = getDbSession()

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

    return {{"data": None}}

@schedule_bp.route('/saveClassDetails_api', methods=['POST', 'GET'])
def saveClassDetails_api():
    try:
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
    except Exception as ex:
        logger.exception(ex)
        return {{'status': 'error', 'message': str(ex)}}

@schedule_bp.route('/deleteClassDetails_api', methods=['POST', 'GET'])
def deleteClassDetails_api():
    delCount = DeleteClass(request.json)
    result = {'status': 'ok', 'message': f'{delCount} class has been deleted'}
    return jsonify(result)

# noinspection PyTestUnpassedFixture
@schedule_bp.route('/print_schedule_api', methods=['POST', 'GET'])
def print_schedule_api():
    try:
        class_records_stmt = (select(Classes)
                              .order_by(Classes.classDayOfWeek)
                              .order_by(cast(Classes.classCheckinStart, Float))
                              )
        class_records       = db_session.scalars(class_records_stmt).all()

        school_details_stmt = (select(Schools)
                               .where(Schools.schoolId == 1)
                               )
        school_record       = db_session.scalars(school_details_stmt).first()

        footer_text         = GetScheduleFooterText()
        PrintClassSchedule(school_record, class_records, footer_text)
        return {"status": 'ok', 'message' : 'Schedule PDF was created'}
    except Exception as ex:
        logger.exception(ex)
        return {"status": 'error', 'message' : str(ex)}

def GetScheduleFooterText() -> list:
    return [
        '*All Classes are subject to change',
        'It is recommended that students attend at least 3 classes per week',
        'Karate Kids 4 to 6 years of age ~ Karate Youth 7 to 10 years of age ~ Juniors 11 to 15 years of age',
        'Adults 16 years of age and up'
    ]