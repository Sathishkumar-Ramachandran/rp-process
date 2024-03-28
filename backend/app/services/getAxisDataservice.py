from flask import Flask

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
            return data
        except Exception as e:
            print("Error occurred while getting Axis Data")
            return str(e)