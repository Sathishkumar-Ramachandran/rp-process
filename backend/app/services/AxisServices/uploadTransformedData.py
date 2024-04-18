from flask import Flask
from datetime import date
from config.mongoConnection import axis_transformed_data_collection

def upload_TransformedData(data):
    today = str(date.today())
    if data:
        try:
            if axis_transformed_data_collection.find_one({"date": today}):
                axis_transformed_data_collection.update_one({"date":today}, {"$set":{"rawDate":data}})
            else:
                data={'date':today, 'rawdata':data}
                axis_transformed_data_collection.insert_one(data)
            
            return "Data uploaded successfully!"
        
        except Exception as e:
            print("Error in uploading the data : ",e)
            return str(e)
    
    else:
        return "No Data to be Uploaded"