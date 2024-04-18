from flask import Flask, request, Blueprint, jsonify, json, session
import requests
from datetime import date
from app.services.getAxisDataservice import getAxisData
from app.services.AxisServices.rawDataupload import upload_rawdata, update_rawdata, updateBank_rawdata
from app.services.AxisServices.uploadTransformedData import upload_TransformedData
from app.services.AxisServices.getTransformedData import get_transformed_data
from app.services.AxisServices.prepareExcel import prepareExcel, send_email
from app.services.AxisServices.updateBankStatus import updateStatus, update_transformeddata
import os
from config.mongoConnection import axis_raw_data_collection

import pandas as pd
axisData = Blueprint('axisdata', __name__)

@axisData.route('/rawdata/axisbank', methods=['GET'])
def get_axisData():
    try:
        getdate = request.args.get('date') 
        if not getdate:
            getdate = None
            #getdate = str(date.today())
        data = getAxisData(getdate)
        return  data, 200
        
    except Exception as e:
        print("Error in getting axis data",e)
        return {
                "status": "failure",
                "message":"Failed to fetch Axis Data"
               },500


           

@axisData.route('/rawdata/axis/upload', methods=['POST'])
def upload_data():
    payload_data = request.get_json()
    
    if payload_data:
        try:
            upload_rawdata(payload_data)
            return {'message': 'File uploaded successfully'}, 201
        except Exception as e:
            return {'error':'There was an issue with the file you tried to upload.'},  500
        
@axisData.route('/rawdata/axis/update', methods=['POST'])
def updateData():
    update_date = request.args.get('date')
    payload_data = request.get_json()
    
    if payload_data:
        try:
            update_rawdata(payload_data, update_date)
            upload_rawdata(payload_data)
            return jsonify({'message': 'Data updated successfully'}), 201
        except Exception as e:
            return jsonify({'error': 'There was an issue with the file you tried to upload.'}), 500
    else:
        return jsonify({'error': 'No payload provided.'}), 400
    
@axisData.route('/rawdata/axis/updatebank', methods=['POST'])
def updatebankData():
    update_date = request.args.get('date')
    payload_data = request.get_json()
    
    if payload_data:
        try:
            update_rawdata(payload_data, update_date)
            updateBank_rawdata(payload_data)
            return jsonify({'message': 'Data updated successfully'}), 201
        except Exception as e:
            return jsonify({'error': 'There was an issue with the file you tried to upload.'}), 500
    else:
        return jsonify({'error': 'No payload provided.'}), 400

@axisData.route("/requests/data/axis/update", methods=["POST"])
def axisUpdate():
    update_date = request.args.get('date')
    payload_data = request.get_json()
    
    if payload_data:
        try:
            update_transformeddata(payload_data, update_date)
            # upload_rawdata(payload_data)
            return jsonify({'message': 'Data updated successfully'}), 201
        except Exception as e:
            return jsonify({'error': 'There was an issue with the file you tried to upload.'}), 500
    else:
        return jsonify({'error': 'No payload provided.'}), 400



@axisData.route('/request/data/axis/update', methods=['POST'])
def AxisUpdate():
    upload_date = request.args.get('date')
    payload_data = request.get_json()

    if payload_data and upload_date:
        try:
            updateStatus(upload_date, payload_data) # Update status of data in
            return jsonify({'message': 'Status Updated Successfully'}), 201
        except Exception as e:
            return  jsonify({'error': f"Error updating status {e}"}), 500
    else:
        return jsonify({'error': 'No payload or Date provided.'}), 400

@axisData.route('/data/axis/upload', methods=['POST'])
def uploadTransformed_data():
    payload_data = request.get_json()
    if payload_data:
        try:
            upload_TransformedData(payload_data)
            return {'message': 'Data Transformed and Uploaded Successfully'} ,201
            
        except ValueError as ve:
            return {"error":str(ve)},   400

@axisData.route('/requests/data/axis', methods=['GET'])
def get_TransformedData():
    try:
        getdate = request.args.get('date') 
        if not getdate:
            getdate = str(date.today())
        data = get_transformed_data(getdate)
        return  data, 200
        
    except Exception as e:
        print("Error in getting axis data",e)
        return {
                "status": "failure",
                "message":"Failed to fetch Axis Data"
               },500
    
def UiPath_Authentication():
    url = "https://account.uipath.com/oauth/token"
    payload = json.dumps({
        "grant_type": "refresh_token",
        "client_id": "8DEv1AMNXczW3y4U15LL3jYf62jK93n5",
        "refresh_token": "_4_g8Wxo4NJrVY2rJH237nwGouFsv6L_gQ8Rdh-mbe9CP"
    })
    headers = {
        'X-UIPATH-TenantName': 'DefaultTenant',
        'Content-Type': 'application/json',
    }
 
    response = requests.request("POST", url, headers=headers, data=payload)
    output = json.loads(response.text)
    # print(output)
    session["uipath_token"] = output["access_token"]
    return jsonify(output)
 

def UiPath_StartJob(releaseKey, arguments):
    UiPath_Authentication()
    url = "https://platform.uipath.com/catnihsiauva/DefaultTenant/odata/Jobs/UiPath.Server.Configuration.OData.StartJobs"  
    payload = json.dumps({
    "startInfo": {
        "ReleaseKey": releaseKey
    }
    })
    headers = {
        'Authorization': 'Bearer '+str(session["uipath_token"]),
        'Content-Type': 'application/json',
        'X-UIPATH-OrganizationUnitId': '4713450',
    }
 
    response = requests.request("POST", url, headers=headers, data=payload)
    output=json.loads(response.text)
    print(output)
    return output


@axisData.route('/updatestatus', methods=['POST'])
def update_status():
    date = request.args.get('date')
    payload = request.get_json()
    # print(date)
    # print(payload)
    if date and payload:
        for data in payload:
            row_data = data.get('row', {})
            merchant_id = row_data.get('MerchantIdentifier')
            print(merchant_id)
            if merchant_id:
                axis_raw_data_collection.update_many(
                    {
                        "date": str(date),
                        "rawdata.data.Merchants ID": str(merchant_id)
                    },
                    {
                        "$set": {
                            "rawdata.$.data.status": "Pending",
                        }
                    } 
                )
               
        return jsonify({"message": "Merchant is is not provided"}), 300
    else:
        return f'Date and Payload is not provided'
    

@axisData.route('/sendmail', methods=['POST'])
def sendMail():
    attachment = request.files.get('file')
    print("Data  "+str(request.form.get('selectedRows')))
    payload = json.loads(str(request.form.get('selectedRows')))  # Adjust to parse selectedRows from form data
    
    # payload=None
    if payload is None:
            raise ValueError("No selectedRows data found in the form.")
    if not payload:
        return jsonify({'error': 'Payload is empty'}), 400

    if attachment and payload:
        attachment_filename = attachment.filename
        attachment_path = os.path.join('attachments', attachment_filename)  # Adjust path as needed
        os.makedirs(os.path.dirname(attachment_path), exist_ok=True)  # Create directory if it doesn't exist
        attachment.save(attachment_path)
        prepareExcel(payload)
        UiPath_StartJob("6bca95f9-6722-45cc-8e49-ca5ff45a7fbb", {})
        
    elif not attachment and payload:
        # Handle payload if no attachment
        prepareExcel(payload)
        UiPath_StartJob("6bca95f9-6722-45cc-8e49-ca5ff45a7fbb", {})
        return 'Mail Sent Successfully', 200

    return 'Mail Sent Successfully', 200

    
# @axisData.route('/sendmail', methods=['POST'])
# def sendMail():
#     attachment = request.files.get('file')
#     payload = request.get_json()

#     if not payload:
#         return jsonify({'error': 'Payload is empty'}), 400

#     if attachment and payload:
#         attachment_filename = attachment.filename
#         attachment_path = os.path.join('./attachments', attachment_filename)
#         attachment.save(attachment_path)
        
#     elif  not attachment and payload:
#         prepareExcel(payload)
#         UiPath_StartJob("6bca95f9-6722-45cc-8e49-ca5ff45a7fbb",{})
#         return f'Mail Sent Successfully'
    
#     # if attachment:
#     #     with open(attachment_path, 'rb') as attachment_file:
#     #         attachment_data = attachment_file.read()
#     #         UiPath_StartJob("6bca95f9-6722-45cc-8e49-ca5ff45a7fbb", {"attachment": attachment_data})
#     #     os.remove(attachment_path)
#     #     return 'Mail Prepared and Sent Successfully', 200

#     # If there is no attachment, just send the payload without attachment
#     #UiPath_StartJob("6bca95f9-6722-45cc-8e49-ca5ff45a7fbb",{})
#     return 'Mail Sent Successfully', 200


# @axisData.route('/sendmail', methods=['POST'])
# def sendMail():
#     attachment = request.files.get('file')
#     payload = request.get_json()
#     if payload and attachment:
#         attachment_data = attachment.read()
#         prepareExcel(payload)
#         UiPath_StartJob("6bca95f9-6722-45cc-8e49-ca5ff45a7fbb", {"attachment": attachment_data})
#         return f'Mail Prepared Successfully'
#     elif attachment:
#         prepareExcel(payload)
#         UiPath_StartJob("6bca95f9-6722-45cc-8e49-ca5ff45a7fbb",{})
#         return f'Mail Sent Successfully'
#     else:
#         return f'Payload is Empty'
    