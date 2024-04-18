from flask import Flask, request, jsonify
from config.mongoConnection import axis_raw_data_collection, axis_transformed_data_collection


def updateStatus(date, payload):
    for data in payload:
        merchant_id = data.get('MerchantIdentifier')
        Bank_Response = data.get('status')
        Remarks = data.get('Remarks')

        axis_raw_data_collection.update_one(
            {
                "date": str(date),
                "rawdata.data.Merchants ID": merchant_id
            },
            {
                "$set": {
                    "rawdata.$.status": "Bank Updated",
                    "rawdata.$.Bank Response": Bank_Response, "rawdata.$.Remarks": Remarks }
            } 
            
        )
        return jsonify({"message": "Status updated successfully"}), 200
    
def update_transformeddata(payload, upload_date):
    if payload:
        try:
            # Delete existing document
            axis_transformed_data_collection.delete_one({"date": upload_date})   
            axis_transformed_data_collection.insert_one({
                "date": upload_date,
                "rawdata": payload

            })         
            return {'message': f'Data for {upload_date} has been updated successfully.'}, 201
        except Exception as e:
            return {'error': str(e)}, 500
    else:
        return {'error': 'Payload is empty'}, 400