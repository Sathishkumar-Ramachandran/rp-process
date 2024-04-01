from flask import Flask, request, Blueprint
from datetime import date
from app.services.KotakServices.uploadKotakRawData import  upload_rawdata
from app.services.KotakServices.getRawData import  get_rawdata

kotakData = Blueprint('kotakData', __name__)
@kotakData.route('/rawdata/kotak/upload' , methods=['POST'])
def upload_Rawdata():
    data = request.get_json()
    if not data:
        return f'Data is not available'
    else:
        try:
            upload_rawdata(data)
            return data
        except Exception as e :
            print("Error in Upload Data")

@kotakData.route('/rawdata/kotakbank', methods=['GET'])
def get_rawdata():
    try:
        getdate = request.args.get('date') 
    
        if not getdate:
            getdate = str(date.today())
        result = get_rawdata(getdate)

        return {'result': result}
    except Exception as e:
        print("Error in getting data :",str(e))
