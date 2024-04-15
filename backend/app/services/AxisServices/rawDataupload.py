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
                updated_payload = [{"slot_number": slot_number, "data": {**row, "status": "Pending"}} for row in payload]
                axis_raw_data_collection.find_one_and_update(
                    {"date": upload_date},
                    {
                        "$push": {"rawdata": {"$each": updated_payload}},
                    },
                    upsert=True
                )
                return {'message': 'Data updated successfully.'}, 201
            else:
                initial_payload = [{"slot_number": 1, "data": {**row, "status": "Pending"}} for row in payload]
                axis_raw_data_collection.insert_one({
                    "date": upload_date,
                    "rawdata": initial_payload
                })
                return {'message': f'Data for {upload_date} has been uploaded Successfully'}, 201
        except Exception as e:
            return {'error': str(e)}, 500
    else:
        return {'error': 'Payload is empty'}, 400


# def upload_rawdata(payload):
#     upload_date = str(date.today())
#     if payload:
#         try:
#             existing_data = axis_raw_data_collection.find_one({"date": upload_date})
#             if existing_data:
#                 slot_number = existing_data['rawdata'][-1]['slot_number'] + 1 if 'rawdata' in existing_data and existing_data['rawdata'] else 1
#                 axis_raw_data_collection.find_one_and_update(
#                     {"date": upload_date},
#                     {
#                         "$push": {"rawdata": {"slot_number": slot_number, "data": payload, "status": "Pending"}},
#                     },
#                     upsert=True
#                 )
#                 return {'message': 'Data updated successfully.'}, 201
#             else:
#                 axis_raw_data_collection.insert_one({
#                     "date": upload_date,
#                     "rawdata": [{"slot_number": 1, "data": payload, "status": "Pending"}]
#                 })
#                 return {'message': f'Data for {upload_date} has been uploaded Successfully'}, 201
#         except Exception as e:
#             return {'error': str(e)}, 500
#     else:
#         return {'error': 'Payload is empty'}, 400
def update_rawdata(payload, upload_date):
    if payload:
        try:
            # Delete existing document
            axis_raw_data_collection.delete_one({"date": upload_date})            
            return {'message': f'Data for {upload_date} has been updated successfully.'}, 201
        except Exception as e:
            return {'error': str(e)}, 500
    else:
        return {'error': 'Payload is empty'}, 400





   
# def update_rawdata(payload,upload_date):
#    # upload_date = str(date.today())
#     if payload:
#         try:
#             existing_data = axis_raw_data_collection.find_one({"date": upload_date})
#             if existing_data:
#                 slot_number = existing_data['rawdata'][-1]['slot_number'] + 1 if 'rawdata' in existing_data and existing_data['rawdata'] else 1
#                 axis_raw_data_collection.replace_one(
#                     {"date": upload_date},
#                     {
#                         "$push": {"rawdata": {"slot_number": slot_number, "data": payload, "status": "Pending"}},
#                     },
#                     upsert=True
#                 )
#                 return {'message': 'Data updated successfully.'}, 201
#             else:
#                 axis_raw_data_collection.insert_one({
#                     "date": upload_date,
#                     "rawdata": [{"slot_number": 1, "data": payload, "status": "Pending"}]
#                 })
#                 return {'message': f'Data for {upload_date} has been uploaded Successfully'}, 201
#         except Exception as e:
#             return {'error': str(e)}, 500
#     else:
#         return {'error': 'Payload is empty'}, 400
    