from flask import Flask
from config.mongoConnection import raw_data_collecction
from datetime import date

def upload_rawdata(rawdata):
    today = date.today()
    try:
        transformed_data = []
        for entry in rawdata:
            transformed_entry = {}
            for key, value in entry.items():
                if key != 'rawDate':
                    transformed_entry[key] = value
                else:
                    transformed_entry.update(value)
            transformed_data.append(transformed_entry)

        raw_data_collecction.insert_one(
            {
                "date": str(today),
                "transformedData": transformed_data
            }
        )
        return {"status": "success", "msg": "Data uploaded successfully"}
    except Exception as e:
        print("Error in data insertion : ", e)
        return {"error": "Error in data insertion"}, 500




# def upload_rawdata(rawdata):
#     today = date.today()
#     try:
#         raw_data_collecction.insert_one(
#             {
#                 "date": str(today),
#                 "rawDate": rawdata
#             }
#         )
#         return {"status":"success", "msg":"Data uploaded successfully"}
#     except Exception as e:
#         print("Error in data insertion : ", e)

