from flask import Flask, request, jsonify
from datetime import date
from config.mongoConnection import kotak_bank_data


def get_kotakdata(look_date):
    today = date.today()
    if look_date:
        try:
            data = kotak_bank_data.find_one(
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
        data = kotak_bank_data.find_one(
            {
                "date": str(today)
            }
        )
        print(data)
        return jsonify(data)