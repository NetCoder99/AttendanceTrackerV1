# ------------------------------------------------------------------
# pyinstaller --add-data "templates;templates" --add-data "static;static" --add-data "students;students" main.py
# ------------------------------------------------------------------
import os
import sys
from flask import Flask, render_template, request, jsonify
from flaskwebgui import FlaskUI

from blueprints.schedule.routes import schedule_bp
from blueprints.students.routes import students_bp
from services.checkin_procs import validateCheckin

# ----------------------------------------------------------------------------------
base_dir = '.'
if hasattr(sys, '_MEIPASS'):
    base_dir = os.path.join(sys._MEIPASS)

# ----------------------------------------------------------------------------------
app = Flask(__name__, static_folder=os.path.join(base_dir, 'static'), template_folder=os.path.join(base_dir, 'templates'))
app.register_blueprint(students_bp)
app.register_blueprint(schedule_bp)

# ----------------------------------------------------------------------------------
@app.route('/')
def index():
    checkinMessage = {
        "imageSrc" : "static/images/misc_images/RSM_Logo1.jpg",
        "message"  : "Waiting ...",
        "responseClass" : "fw-bold border-bottom error"}
    return render_template('index.html', checkinMessage=checkinMessage)

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/checkin', methods=['POST'])
def checkin():
    if request.method == 'POST':
        data = request.form.to_dict()
        return jsonify(validateCheckin(request.form.to_dict()))

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
    #ui = FlaskUI(app=app, width=1200, height=900, fullscreen=False, server='flask')
    #ui.run()
    app.run(debug=False)