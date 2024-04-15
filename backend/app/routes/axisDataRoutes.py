from flask import Flask, request, Blueprint, jsonify, json, session
import requests
from datetime import date
from app.services.getAxisDataservice import getAxisData
from app.services.AxisServices.rawDataupload import upload_rawdata, update_rawdata
from app.services.AxisServices.uploadTransformedData import upload_TransformedData
from app.services.AxisServices.getTransformedData import get_transformed_data
from app.services.AxisServices.prepareExcel import prepareExcel, send_email

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

# @axisData.route('/rawdata/axis/update', methods=['POST'])
# def updateData():
#     update_date = request.args.get('date')
#     payload_data = request.get_json()
    
#     if payload_data:
#         try:
#             update_rawdata(payload_data, update_date)
#             return {'message': 'File uploaded successfully'}, 201
#         except Exception as e:
#             return {'error':'There was an issue with the file you tried to upload.'},  500
        


@axisData.route('/data/axis/upload', methods=['POST'])
def uploadTransformed_data():
    payload_data = request.get_json()
    if payload_data:
        try:
            upload_TransformedData(payload_data)
            return {'message': 'Data Transformed and Uploaded Successfully'} ,201
            
        except ValueError as ve:
            return {"error":str(ve)},   400

@axisData.route('/data/axis', methods=['GET'])
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
    session["uipath_token"] = output["access_token"]
    return jsonify(output)
 

def UiPath_StartJob(releaseKey, arguments):
    UiPath_Authentication()
    url = "https://platform.uipath.com/catnihsiauva/DefaultTenant/odata/Jobs/UiPath.Server.Configuration.OData.StartJobs"  
    payload = json.dumps({
    "startInfo": {
        "ReleaseKey": releaseKey, 
        "Strategy": "Specific",
        "InputArguments": arguments
    }
    })
    headers = {
        'Authorization': 'Bearer '+str(session["uipath_token"]),
        'Content-Type': 'application/json',
        'X-UIPATH-OrganizationUnitId': '4713450',
    }
 
    response = requests.request("POST", url, headers=headers, data=payload)
    output=json.loads(response.text)
    return output

@axisData.route('/sendmail', methods=['POST'])
def sendMail():
    payload = request.get_json()
    if payload:
        prepareExcel(payload)
        UiPath_StartJob("6bca95f9-6722-45cc-8e49-ca5ff45a7fbb", {})
        return f'Mail Prepared Successfully'
    else:
        return f' Payload is Empty'
    