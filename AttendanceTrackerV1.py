# ------------------------------------------------------------------
# pyinstaller --add-data "templates;templates" --add-data "static;static" --add-data "blueprints/students;blueprints/students" --add-data "blueprints/schedule;blueprints/schedule" --add-data "blueprints/belts;blueprints/belts" AttendanceTrackerV1.py
# pyinstaller --add-data "templates:templates" --add-data "static:static" --add-data "blueprints/students:blueprints/students" --add-data "blueprints/schedule:blueprints/schedule" --add-data "blueprints/belts:blueprints/belts" AttendanceTrackerV1.py
# ------------------------------------------------------------------
# rsync -av --exclude '.venv' --exclude 'dist'  --exclude 'build' /home/johnd/AttendanceTracker/AttendanceTrackerV1 /media/johnd/USB31FD/PythonProjects/AttendanceTrackerV1

import os
import sys
from flask import Flask, render_template, request, jsonify, redirect, url_for, Blueprint
from flask_htmx import HTMX
from flaskwebgui import FlaskUI
import tkinter as tk
from tkinter import messagebox

import constants
from blueprints.belts.routes import belts_bp
from blueprints.schedule.routes import schedule_bp
from blueprints.students.routes import students_bp
from blueprints.requirements.routes import requirements_bp
from services.processScanner import DisplayActiveProcesses, IsProcessActive

# ----------------------------------------------------------------------------------
base_dir = '.'
if hasattr(sys, '_MEIPASS'):
    base_dir = os.path.join(sys._MEIPASS)

# ----------------------------------------------------------------------------------
app = Flask(__name__, static_folder=os.path.join(base_dir, 'static'), template_folder=os.path.join(base_dir, 'templates'))
app.register_blueprint(students_bp)
app.register_blueprint(schedule_bp)
app.register_blueprint(belts_bp)
app.register_blueprint(requirements_bp)

htmx = HTMX(app)

# ----------------------------------------------------------------------------------
@app.route('/')
def index():
    return redirect(url_for('students_bp.students_bp_home'))

@app.route('/about')
def about():
    return render_template('students.html')

@app.errorhandler(404)
@app.errorhandler(500)
def page_not_found(e):
    missing_url = None
    try:
        if request is not None:
            missing_url = request.url
    except Exception as ex:
        print(f'exception:{ex}')
    app.logger.error(f"page_not_found:{e}\n{missing_url}")
    if missing_url is None:
        return render_template("error.html",message="Page not found")
    else:
        return render_template("error.html",message="Page not found", original_message=missing_url)

# Run the application
if __name__ == '__main__':
    DisplayActiveProcesses('attendance')
    ok_to_start = IsProcessActive(constants.applicationName)

    if ok_to_start['status'] == 'ok':
        ui = FlaskUI(app=app, width=1250, height=900, fullscreen=False, server='flask', port=5001)
        ui.run()
    else:
        root = tk.Tk()
        root.withdraw()
        messagebox.showinfo("AttendanceCheckin - Error", ok_to_start['message'])
        print(ok_to_start['message'])

    #app.run(debug=False, port=5001)