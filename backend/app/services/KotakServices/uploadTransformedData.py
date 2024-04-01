from flask import Flask, request
from datetime import date
from config.mongoConnection import kotak_bank_data


def upload_transformedData(data):
    today = str(date.today())
    if data:
        try:
            if kotak_bank_data.find_one({"date": today}):
                kotak_bank_data.update_one({"date":today}, {"$set":{"data":data}})
            else:
                data={'date':today, 'data':data}
                kotak_bank_data.insert_one(data)
            
            return "Data uploaded successfully!"
        
        except Exception as e:
            print("Error in uploading the data : ",e)
            return str(e)
    
    else:
        return "No Data to be Uploaded"