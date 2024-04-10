from flask import Flask, request
from datetime import date
from config.mongoConnection import kotak_raw_data

def upload_requestedDataKotak(payload):
    upload_date = str(date.today())
    if payload:
        try:
            existing_data = kotak_raw_data.find_one({"date": upload_date})
            if existing_data:
                slot_number = existing_data['rawdata'][-1]['slot_number'] + 1 if 'rawdata' in existing_data and existing_data['rawdata'] else 1
                kotak_raw_data.find_one_and_update(
                    {"date": upload_date},
                    {
                        "$push": {"rawdata": {"slot_number": slot_number, "data": payload, "status": "Pending"}},
                    },
                    upsert=True
                )
                return {'message': 'Data updated successfully.'}, 201
            else:
                kotak_raw_data.insert_one({
                    "date": upload_date,
                    "rawdata": [{"slot_number": 1, "data": payload, "status": "Pending"}]
                })
                return {'message': f'Data for {upload_date} has been uploaded Successfully'}, 201
        except Exception as e:
            return {'error': str(e)}, 500
    else:
        return {'error': 'Payload is empty'}, 400