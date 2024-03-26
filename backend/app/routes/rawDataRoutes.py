from flask import Flask, request, Blueprint

from app.services.uploadRawdataService import upload_rawdata
from app.services.getRawdataService import get_rawdata
rawdata = Blueprint('rawdata', __name__)

@rawdata.route('/rawdata/upload', methods=['POST'])
def users_index():
    payload_data = request.get_json()
    if payload_data:
        try:
            upload_rawdata(payload_data)
            return {"message": "Data uploaded successfully."}, 201
        except Exception as e:
            print("Error during uploading rawdata : ", str(e))
    return 'Welcome to the user management page!'

@rawdata.route('/rawdata', methods=['GET'])
def get_rawdata(date):
    try:
        result = get_rawdata()
        return {'result': result}
    except Exception as e:
        print("Error in getting data :",str(e))



