import json
import copy

from flask import Blueprint, render_template, request, jsonify

from sqlite.sqlite_schedule import GetClassRecords

schedule_bp = Blueprint(
    'schedule_bp', __name__,
    template_folder='templates',
    static_folder='static'
)

@schedule_bp.route('/schedule')
def schedule_bp_home():
    class_records = GetClassRecords()
    return render_template('schedule.html')

@schedule_bp.route('/schedule_api', methods=['POST'])
def schedule_bp_api():
    class_records = GetClassRecords()
    return jsonify({"data": class_records})

