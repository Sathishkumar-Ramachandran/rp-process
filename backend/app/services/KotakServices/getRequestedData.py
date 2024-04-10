from flask import Flask, request, jsonify
from config.mongoConnection import kotak_bank_data

def getRequestedDataKotak(date):
    try:
        if date:
            print("Checking existing data")
            data = kotak_bank_data.find_one({"date": date}, {"_id": 0})
     
            return data
        else:
            return jsonify({'message': 'No data found for the specified date.'}), 404
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500
