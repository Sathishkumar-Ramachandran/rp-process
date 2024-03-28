from flask import Flask, jsonify
from config.mongoConnection import raw_data_collecction
from datetime import date

def get_rawdata_func(look_date):
    today = date.today()
    if look_date:
        try:
            data = raw_data_collecction.find_one(
                {
                    "date": look_date
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
        data = raw_data_collecction.find_one(
            {
                "date": str(today)
            }
        )
        print(data)
        return jsonify(data)

