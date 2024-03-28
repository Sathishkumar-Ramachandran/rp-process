from flask import Flask, request, Blueprint
from datetime import date
from app.services.getAxisDataservice import getAxisData
from app.services.AxisServices.rawDataupload import upload_rawdata


axisData = Blueprint('axisdata', __name__)

@axisData.route('/rawdata/axis', methods=['GET'])
def get_axisData():
    try:
        getdate = request.args.get('date') 
        if not getdate:
            getdate = str(date.today())
        data = getAxisData(getdate)
        return  data, 200
        
    except Exception as e:
        print("Error in getting axis data",e)
        return {
                "status": "failure",
                "message":"Failed to fetch Axis Data"
               },500


           

@axisData.route('/rawdata/axis/upload', methods=['POST'])
def upload_data():
    payload_data = request.get_json()
    if payload_data:
        try:
            upload_rawdata(payload_data)
            return {'message': 'File uploaded successfully'}, 201
        except Exception as e:
            print("Unexpected error:", e)
            return {'error':'There was an issue with the file you tried to upload.'},  500