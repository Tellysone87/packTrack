from flask import Flask, render_template, request

from pprint import pformat
import os
import requests
from datetime import datetime



def getBearerAuthorization():
    """ This function gets authorization to the fed ex api"""
    API_KEY = os.environ['FedEx_Api_key']
    client_secret = os.environ['SECRET_KEY']

    # url to bearer authorization
    url = "https://apis-sandbox.fedex.com/oauth/token"

    # sending grant type , api key and secret key
    payload = 'grant_type=client_credentials&client_id='+API_KEY +'&client_secret='+client_secret

    # type of string we want back 
    headers = {
        'Content-Type':"application/x-www-form-urlencoded"
        }

    # making a request
    response = requests.request("POST",url, data=payload, headers=headers)

    # gets access token
    authorization = (response.json()["access_token"])

    #return that token for access
    return authorization


def get_tracking_info(tracking_number):
# token is present. no problem getting tokens. 
    auth = getBearerAuthorization()
    token = auth
    info = {}

    url = "https://apis-sandbox.fedex.com/track/v1/trackingnumbers"
    package_to_track = tracking_number

    # sends authorization key
    headers = {
            'Content-Type': "application/json",
            'Authorization': "Bearer "+token
            }

    # requests info and gets reponse
    payload = '{ "trackingInfo": [ { "trackingNumberInfo": { "trackingNumber": "'+package_to_track+'" } } ], "includeDetailedScans": true }'
    response = requests.post(url, data= payload, headers=headers)

    # grabs tracking number to display
    trackingNumber = response.json()['output']['completeTrackResults'][0]['trackingNumber']

    #grabs the package shipped
    dates = response.json()['output']['completeTrackResults'][0]['trackResults'][0]['dateAndTimes']

    for date in dates:
        if date['type'] == 'SHIP':
            date_str = date['dateTime'][0:10]
            # shipped_on = datetime.strptime(date['dateTime'],"%Y-%m-%d") # time object
    # print(shipped_on)
    # shipped_on = datetime.date(date_shipped)

    #grabs the delivery status
    deliveryStatus = response.json()['output']['completeTrackResults'][0]['trackResults'][0]['latestStatusDetail']['description']
    merchant = ""
    carrier = "FexEX"

    #gets the last known location
    city = response.json()['output']['completeTrackResults'][0]['trackResults'][0]['latestStatusDetail']['scanLocation']['city']
    state = response.json()['output']['completeTrackResults'][0]['trackResults'][0]['latestStatusDetail']['scanLocation']['stateOrProvinceCode']
    location = f"{city}, {state}"

    # sets values for variables if item was delivered or not
    if deliveryStatus == "Delivered":
        recievedByName = response.json()['output']['completeTrackResults'][0]['trackResults'][0]['deliveryDetails']['receivedByName']
        scanEvent = response.json()['output']['completeTrackResults'][0]['trackResults'][0]['scanEvents'][0]
        dateDelivered = scanEvent['date'][0:10]
    else:
        recievedByName=""
        dateDelivered=""

    info['tracking'] = trackingNumber
    info['shipped'] = date_str
    info['location'] = location
    info['status'] = deliveryStatus
    info['merchant'] = ""
    info['carrier'] = "FedEx"

    # shows key information
    # print([trackingNumber,date_str,deliveryStatus,recievedByName,dateDelivered,location])
    # write library to file
    # write_file = open('Api.json','w')
    # write_file.write(response.text)
    # write_file.close()
    return info

print(get_tracking_info(str(394940539699)))
