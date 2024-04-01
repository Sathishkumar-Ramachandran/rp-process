from flask import Flask, request, Blueprint, jsonify, session
import requests
import json
from datetime import time

# Assuming that the UiPath authentication, job start, and job status functions are defined in the same file

botApi = Blueprint('botapi', __name__)

def UiPath_Authentication():
    url = "https://account.uipath.com/oauth/token"
    payload = json.dumps({
        "grant_type": "refresh_token",
        "client_id": "client Id from Orch",
        "refresh_token": "Token from Orch"
    })
    headers = {
        'X-UIPATH-TenantName': 'DefaultTenant',
        'Content-Type': 'application/json',
    }
 
    response = requests.request("POST", url, headers=headers, data=payload)
    output = json.loads(response.text)
    session["uipath_token"] = output["access_token"]
    return jsonify(output)
 
 
 
def UiPath_StartJob(releaseKey,arguments):
    UiPath_Authentication()
    url = "https://platform.uipath.com/catnignyiono/DefaultTenant/odata/Jobs/UiPath.Server.Configuration.OData.StartJobs" 
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
        'X-UIPATH-OrganizationUnitId': '651567',
    }
 
    response = requests.request("POST", url, headers=headers, data=payload)
    output=json.loads(response.text)
    return output
 
 
 
def UiPath_GetJobStatus(jobID):
    url = "https://platform.uipath.com/catnignyiono/DefaultTenant/odata/Jobs("+str(jobID)+")" 
    payload = {}
    headers = {
        'Authorization': 'Bearer '+str(session["uipath_token"]),
        'Content-Type': 'application/json',
        'X-UIPATH-OrganizationUnitId': '651567', 
    }
 

@botApi.route("/triggerbot", methods=["POST"])
def triggerBot():
    # Get the data sent by the client
    data = request.get_json()

    # Extract the release key and arguments from the client data
    release_key = data.get('release_key')
    arguments = data.get('arguments')

    # Authenticate with UiPath and get an access token
    UiPath_Authentication()

    # Start a UiPath job with the provided release key and arguments
    job_start_response = UiPath_StartJob(release_key, arguments)

    # Extract the job ID from the job start response
    job_id = job_start_response.get('Id')

    # Loop until the job is completed
    while True:
        # Get the status of the job
        job_status_response = UiPath_GetJobStatus(job_id)

        # Extract the job state from the job status response
        job_state = job_status_response.get('State')

        # If the job is completed, break out of the loop
        if job_state == 'Completed':
            break

        # Wait for a short period of time before checking the job status again
        time.sleep(5)

    # Return a response indicating that the job has completed
    return jsonify({'message': 'Job completed', 'job_id': job_id})