from flask import Flask
from config.mongoConnection import axis_raw_data_collection
from datetime import date


def upload_rawdata(payload):
    upload_date = str(date.today())
    if payload:
        try:
            existing_data = axis_raw_data_collection.find_one({"date": upload_date})
            if existing_data:
                slot_number = existing_data['rawdata'][-1]['slot_number'] + 1 if 'rawdata' in existing_data and existing_data['rawdata'] else 1
                axis_raw_data_collection.find_one_and_update(
                    {"date": upload_date},
                    {
                        "$push": {"rawdata": {"slot_number": slot_number, "data": payload, "status": "Pending"}},
                    },
                    upsert=True
                )
                return {'message': 'Data updated successfully.'}, 201
            else:
                axis_raw_data_collection.insert_one({
                    "date": upload_date,
                    "rawdata": [{"slot_number": 1, "data": payload, "status": "Pending"}]
                })
                return {'message': f'Data for {upload_date} has been uploaded Successfully'}, 201
        except Exception as e:
            return {'error': str(e)}, 500
    else:
        return {'error': 'Payload is empty'}, 400
    # uploadDate = str(date.today())
    # if payload:
    #     try:
    #         if axis_raw_data_collection.find_one({"date": uploadDate}):
    #             axis_raw_data_collection.update_one({
    #                 "date: ": uploadDate}, {"$push": {"rawDate": payload} 
    #             })
    #         else:
    #             print("Going to direct insert")
    #             axis_raw_data_collection.insert_one({
    #                 'date': uploadDate,
    #                 'rawDate': payload
    #             })
    #             return {'message': f'Data for {uploadDate} has been uploaded Successfully'}
    #     except Exception as e:
    #         return f'Error occured during  data insertion - {e}'