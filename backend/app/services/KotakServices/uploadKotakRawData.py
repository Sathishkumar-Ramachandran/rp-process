from flask import Flask, request
from config.mongoConnection import kotak_raw_data
from datetime import date

def upload_rawdata(payload):
    uploadDate = str(date.today())
    if payload:
        try:
            if kotak_raw_data.find_one({"date": uploadDate}):
                kotak_raw_data.update_one({
                    "date: ": uploadDate}, {"$push": {"rawdata": payload} 
                })
            else:
                print("Going to direct insert")
                kotak_raw_data.insert_one({
                    'date': uploadDate,
                    'rawdata': payload
                })
                return {'message': f'Data for {uploadDate} has been uploaded Successfully'}
        except Exception as e:
            return f'Error occured during  data insertion - {e}'
    