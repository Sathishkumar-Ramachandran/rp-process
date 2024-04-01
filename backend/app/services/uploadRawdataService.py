from flask import Flask
from config.mongoConnection import raw_data_collecction
from datetime import date
 
def upload_rawdata(rawdata):
    today = str(date.today())
    if rawdata:
        try:
            if raw_data_collecction.find_one({"date": today}):
                raw_data_collecction.update_one({"date":today}, {"$set":{"rawDate":rawdata}})
            else:
                data={'date':today, 'rawDate':rawdata}
                raw_data_collecction.insert_one(data)
            
            return "Data uploaded successfully!"
        
        except Exception as e:
            print("Error in uploading the data : ",e)
            return str(e)
    
    else:
        return "No Data to be Uploaded"