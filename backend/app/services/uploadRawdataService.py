from flask import Flask
from config.mongoConnection import raw_data_collecction
from datetime import date

def upload_rawdata(rawdata):
    today = date.today()
    try:
        raw_data_collecction.insert_one(
            {
                "date": str(today),
                "rawDate": rawdata
            }
        )
        return {"status":"success", "msg":"Data uploaded successfully"}
    except Exception as e:
        print("Error in data insertion : ", e)

