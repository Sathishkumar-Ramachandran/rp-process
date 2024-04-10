from flask import Flask, request, Blueprint, jsonify
from datetime import date
from app.services.KotakServices.uploadKotakRawData import  upload_rawdata
from app.services.KotakServices.getRawData import  get_rawdata
from app.services.KotakServices.uploadTransformedData import upload_transformedData
from app.services.KotakServices.getTransformedData  import get_kotakdata
from app.services.KotakServices.getRequestedData import getRequestedDataKotak
from app.services.KotakServices.uploadRequestedData import upload_requestedDataKotak

kotakData = Blueprint('kotakData', __name__)
@kotakData.route('/rawdata/kotak/upload' , methods=['POST'])
def upload_Rawdata():
    data = request.get_json()
    if not data:
        return f'Data is not available'
    else:
        try:
            upload_requestedDataKotak(data)
            #upload_rawdata(data)
            return data
        except Exception as e :
            print("Error in Upload Data")

@kotakData.route('/rawdata/kotakbank', methods=['GET'])
def get_rawdata():
    try:
        getdate = request.args.get('date') 
    
        if not getdate:
            getdate = str(date.today())
        result = getRequestedDataKotak(str(getdate))
        return jsonify(result)
    except Exception as e:
        print("Error in getting data:", str(e))
        return jsonify({'error': str(e)}), 500
@kotakData.route('/data/kotak/upload', methods=['POST'])
def upload_transformedData():
    data = request.get_json()
    if not data:
        return f'Data is not available'
    else:
        try:
            upload_requestedDataKotak(data)
            #upload_transformedData(data)
            return data
        except Exception as e :
            print("Error in Upload Data")


@kotakData.route('/data/kotak', methods=['GET'])
def getTransformedData():
    try:
        getdate = request.args.get('date') 
    
        if not getdate:
            getdate = str(date.today())
        result = get_kotakdata(getdate)

        return {'result': result}
    except Exception as e:
        print("Error in getting data :",str(e))


@kotakData.route('/requests/kotakbank',  methods=['GET'])
def getRequestedData():
    try:
        getdate = request.args.get('date')
        print(getdate)
        if not getdate:
            getdate = str(date.today())
        
        result = getRequestedDataKotak(getdate)
        return result
    except Exception as e: 
        return jsonify({"error": "Error in Getting Requested Kotak Bank Data"}, 500)
    

@kotakData.route("/requests/kotakbank/", methods=['POST'])
def addRequest():
    req_data = request.get_json()
    print(req_data)
    try:
        upload_requestedDataKotak(req_data)  
        return {"message":"Successfully added to database"},201
    except Exception as e:
        return {"error": f"Failed to Add the data {str(e)}"},500