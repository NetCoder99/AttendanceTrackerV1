import json
import copy

from flask import Blueprint, render_template, request, jsonify

from sqlite.sqlite_schedule import GetClassRecords, GetClassRecordsSorted

schedule_bp = Blueprint(
    'schedule_bp', __name__,
    template_folder='templates',
    static_folder='static',
    static_url_path='/schedule_bp_static'
)

@schedule_bp.route('/schedule')
def schedule_bp_home():
    class_records = GetClassRecordsSorted()
    return render_template('schedule.html')

@schedule_bp.route('/schedule_api', methods=['POST', 'GET'])
def schedule_bp_api():
    class_records = GetClassRecordsSorted()
    return jsonify({"data": class_records})

