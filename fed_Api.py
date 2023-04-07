from flask import Flask, render_template, request

from pprint import pformat
import os
import requests



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

# token is present. no problem getting tokens. 
auth = getBearerAuthorization()
token = auth
print(token)

url = "https://apis-sandbox.fedex.com/track/v1/trackingnumbers"
trackingNumber = str(394940539699)

headers = {
        'Content-Type': "application/json",
        'Authorization': "Bearer "+token
        }

payload = '{ "trackingInfo": [ { "trackingNumberInfo": { "trackingNumber": "'+trackingNumber+'" } } ], "includeDetailedScans": true }'
response = requests.post(url, data= payload, headers=headers)

print(trackingNumber)
print(response.text)
