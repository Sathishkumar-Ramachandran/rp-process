from flask import Flask,jsonify,json

from config.mongoConnection import axis_raw_data_collection

def getAxisData(date):
    if not date:
        return "Date is not provided to fetch"
    else:
        try:
            data = axis_raw_data_collection.find_one({
                "date": date
            },
            {
                '_id': 0
            })
            with open("./sample.json", "w") as json_file:     
                json.dump(data, json_file)
            print(data)
            return jsonify(data)
        except Exception as e:
            print("Error occurred while getting Axis Data")
            return str(e)