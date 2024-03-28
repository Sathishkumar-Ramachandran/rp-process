from flask import Flask, request, Blueprint
from datetime import date
from app.services.getAxisDataservice import getAxisData
axisData = Blueprint('axisdata', __name__)

@axisData.route('/rawdata/axis/<getdate>', methods=['GET'])
def get_axisData(getdate):
    if not getdate:
        get_date = date.today()
        try:
            getAxisData(get_date)
            return  {"status": "success", 200: 'Requested data for today.'},  200
        except Exception as e:
            return f'Error Occured during Axis Data Retrieval', 400

@axisData.route('/rawdata/axis', methods=['POST'])