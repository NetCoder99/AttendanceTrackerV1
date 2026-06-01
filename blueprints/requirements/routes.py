from flask import Blueprint, render_template, request, jsonify

from sqlite.sqlite_procs import GetDataNoArgs

requirements_bp = Blueprint(
    'requirements_bp', __name__,
    template_folder='templates',
    static_folder='static',
    static_url_path='/requirements_bp_static'
)

@requirements_bp.route('/requirements')
def schedule_bp_home():
    return render_template('requirements_list.html')

@requirements_bp.route('/getRequirementsList_api')
def getRequirementsList_api():
    print(f'getRequirementsList_api')
    requirements_records = GetDataNoArgs(GetRequirementsListStmt())
    return jsonify({"data":requirements_records})

def GetRequirementsListStmt():
    return '''
        select
            r.requirementId,
            r.beltId,
            b.beltTitle,
            r.stripeTitle,
            r.requiredClasses,
            r.createDateTime
        from requirements   r
        join belts b
          on r.beltId = b.beltId
        order  by r.beltId, r.stripeId      
    '''
# # ----------------------------------------------------------------------------
# def GetDataNoArgs(queryStmt):
#     try:
#         db_path = getDbPath()
#         dbObj = sqlite3.connect(db_path)
#         dbObj.row_factory = DictFactory
#         cursor = dbObj.cursor()
#         cursor.execute(queryStmt)
#         rows = cursor.fetchall()
#         dbObj.close()
#         return rows
#     except Exception as ex:
#         print(f'Error: {ex.__str__()}')
