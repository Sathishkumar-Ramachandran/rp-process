from flask import Flask
from config.mongoConnection import axis_raw_data_collection
from datetime import date


def upload_rawdata(payload):
    uploadDate = str(date.today())
    if payload:
        try:
            if axis_raw_data_collection.find_one({"date": uploadDate}):
                axis_raw_data_collection.update_one({
                    "date: ": uploadDate}, {"$push": {"rawdata": payload} 
                })
            else:
                print("Going to direct insert")
                axis_raw_data_collection.insert_one({
                    'date': uploadDate,
                    'rawdata': payload
                })
                return {'message': f'Data for {uploadDate} has been uploaded Successfully'}
        except Exception as e:
            return f'Error occured during  data insertion - {e}'