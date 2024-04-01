from flask import Flask, jsonify
from config.mongoConnection import kotak_raw_data
from datetime import date

def get_rawdata(look_date):
    today = date.today()
    if look_date:
        try:
            data = kotak_raw_data.find_one(
                {
                    "date": str(look_date)
                },
                {
                    "_id": 0
                }
            )
            
            return data
        except Exception as e:
            print("Error in getting data : ",e)
            return False
    else:
        data = kotak_raw_data.find_one(
            {
                "date": str(today)
            }
        )
        print(data)
        return jsonify(data)

