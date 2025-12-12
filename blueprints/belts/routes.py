import json
import copy

from flask import Blueprint, render_template, request, jsonify

from blueprints.belts.sqlite_belts import *

belts_bp = Blueprint(
    'belts_bp', __name__,
    template_folder='templates',
    static_folder='static',
    static_url_path='/belts_bp_static'
)

@belts_bp.route('/belts')
def schedule_bp_home():
    #class_records = GetClassRecordsSorted()
    return render_template('belts_list.html')

@belts_bp.route('/getRanksList_api', methods=['POST', 'GET'])
def getRanksList_api():
    ranksRecords = GetRanksRecords()
    return jsonify({"data": ranksRecords})

@belts_bp.route('/getBeltsList_api', methods=['POST', 'GET'])
def getBeltsList_api():
    beltsRecords = GetBeltsRecords()
    return jsonify({"data": beltsRecords})

@belts_bp.route('/getStripesList_api', methods=['POST', 'GET'])
def getStripesList_api():
    searchData = request.json
    beltsRecords = GetStripeRecords(searchData)
    return jsonify({"data": beltsRecords})

@belts_bp.route('/addNextStripe_api', methods=['POST', 'GET'])
def addNextStripe_api():
    searchData = request.json
    nextPrefix = GetNextStripeName(searchData)
    print(f'searchData: {searchData['rankNum']}, nextPrefix: {nextPrefix}')
    if len(nextPrefix) > 0:
        insData = {
            'stripeName' : nextPrefix[0]['stripeName'],
            'rankNum'    : nextPrefix[0]['rankNum'],
            'classCount' : nextPrefix[0]['stripeClassCount'],
            'seqNum'     : nextPrefix[0]['seqNum']
        }
        lastRowId = InsStripeRecord(insData)
        nextPrefix[0]['lastRowId'] = lastRowId
        return nextPrefix[0]
    else:
        return {"data": ""}

@belts_bp.route('/delStripe_api', methods=['POST', 'GET'])
def delStripe_api():
    searchData = request.json
    DelStripeRecord(searchData)
    #print(f'searchData: {json.dumps(searchData)}')
    return {"data": ""}

