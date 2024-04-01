from flask import Flask, request, jsonify
from datetime import date
from config.mongoConnection import axis_transformed_data_collection

def get_transformed_data(look_date):
    today = date.today()
    if look_date:
        try:
            data = axis_transformed_data_collection.find_one(
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
        data = axis_transformed_data_collection.find_one(
            {
                "date": str(today)
            }
        )
        print(data)
        return jsonify(data)