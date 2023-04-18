"""
    This python file was created to successfully interact with the FedEx Tracking API. I am able to use the created funtions ton make calls 
    to collect package tracking information. 

    getBearerAuthorization() - gets the security token to recognize the user and app that is sending requests to the Api. This is needed for calls and 
    expires after an hour.

    get_tracking_info(tracking_number): - Is the actual call to the Api, it returns the library needed to create a new oackage object. 

"""
# import needed libraries
import os
import requests
from datetime import datetime

def getBearerAuthorization():
    """ This function gets authorization to the fed ex api by returning a bearer token. Be sure to run secret.sh before calling until I implement auto running"""

    # Variables needed collected from secrets.sh. 
    # I created a FedEx account to obtain an API Key and Secret Client
    API_KEY = os.environ['FedEx_Api_key']
    client_secret = os.environ['SECRET_KEY']

    # url to bearer authorization
    url = "https://apis-sandbox.fedex.com/oauth/token"

    # sending grant type, api key and secret key
    payload = 'grant_type=client_credentials&client_id='+API_KEY +'&client_secret='+client_secret

    
    headers = {
        # type of string we want back 
        'Content-Type':"application/x-www-form-urlencoded"
        }

    # making a request that returns a json library with authorization data for my FedEx account.
    response = requests.request("POST",url, data=payload, headers=headers)

    # gets access token from the json file at key [access token]
    authorization = (response.json()["access_token"])

    #return that token for access
    return authorization


def get_tracking_info(tracking_number):
# auth contains the authorization token returned from the function getBearerAuthorization()
    auth = getBearerAuthorization()
    token = auth # Token to make requests to the FedEx Api
    info = {} # setting an empty library to create my own library based on the data I need pulled from the requests json

    url = "https://apis-sandbox.fedex.com/track/v1/trackingnumbers" # url for the tracking library
    package_to_track = tracking_number # this grabs the tracking number passed by the user in the server on tracking.html as the argument

    # sends authorization key
    headers = {
            'Content-Type': "application/json", # type of string we want back 
            'Authorization': "Bearer "+token # Account/App authorization
            }

    # requests info and gets reponse. We passed the giving tracking number to the api and it returns the info for that package
    payload = '{ "trackingInfo": [ { "trackingNumberInfo": { "trackingNumber": "'+package_to_track+'" } } ], "includeDetailedScans": true }'
    response = requests.post(url, data= payload, headers=headers) # json based on that tracking number

    # grabs tracking number to display
    trackingNumber = response.json()['output']['completeTrackResults'][0]['trackingNumber']

    # grabs the package shipped dates
    dates = response.json()['output']['completeTrackResults'][0]['trackResults'][0]['dateAndTimes']

    # loops through the dates and grabs the date with the event equal to SHIP. 
    for date in dates:
        if date['type'] == 'SHIP':
            date_str = date['dateTime'][0:10]
            # shipped_on = datetime.strptime(date['dateTime'],"%Y-%m-%d") # time object
   
    #grabs the delivery status
    deliveryStatus = response.json()['output']['completeTrackResults'][0]['trackResults'][0]['latestStatusDetail']['description']

    # Only using FedEx api for now and the merchant is not available. I am setting default values for now
    merchant = ""
    carrier = "FedEx"

    #gets the last known location
    city = response.json()['output']['completeTrackResults'][0]['trackResults'][0]['latestStatusDetail']['scanLocation']['city']
    state = response.json()['output']['completeTrackResults'][0]['trackResults'][0]['latestStatusDetail']['scanLocation']['stateOrProvinceCode']

    # combining the city and state into one. 
    location = f"{city}, {state}"

    # adding the needed values to my personal info library that will be the return
    info['tracking'] = trackingNumber
    info['shipped'] = date_str
    info['location'] = location
    info['status'] = deliveryStatus
    info['merchant'] = merchant
    info['carrier'] = carrier

    return info #return my library for creating the package object instance


def get_events_info(tracking_number):
# auth contains the authorization token returned from the function getBearerAuthorization()
    auth = getBearerAuthorization()
    token = auth # Token to make requests to the FedEx Api
    history = {} # setting an empty library to create my own library based on the data I need pulled from the requests json
    url = "https://apis-sandbox.fedex.com/track/v1/trackingnumbers" # url for the tracking library
    package_to_track = tracking_number # this grabs the tracking number passed by the user in the server on tracking.html as the argument

    # sends authorization key
    headers = {
            'Content-Type': "application/json", # type of string we want back 
            'Authorization': "Bearer "+token # Account/App authorization
            }

    # requests info and gets reponse. We passed the giving tracking number to the api and it returns the info for that package
    payload = '{ "trackingInfo": [ { "trackingNumberInfo": { "trackingNumber": "'+package_to_track+'" } } ], "includeDetailedScans": true }'
    response = requests.post(url, data= payload, headers=headers) # json based on that tracking number

    # grabs tracking number to display
    # trackingNumber = response.json()['output']['completeTrackResults'][0]['trackingNumber']

    #grabs the delivery status
    events_statuses = response.json()['output']['completeTrackResults'][0]['trackResults'][0]['scanEvents']
    event_num = 0
    #loop through each event and grab the data
    for events in events_statuses:

        # set the values for the dictionary values
        date = events['date'][0:10]
        event = events['eventDescription']
        city_location = events['scanLocation'].get('city')
        state_location = events['scanLocation'].get('stateOrProvinceCode')

        #create new empty dictionary and add values
        events_library = {}
        events_library['track'] = package_to_track
        events_library['date'] = date
        events_library['event'] = event
        events_library['location'] = f'{city_location}, {state_location}'

        # condition if the location is None
        if events_library['location'] == 'None, None':
            events_library['location'] = 'Unknown'
        
    
        # Add the dictionary to my history dictionary
        history[event_num] = events_library
        event_num +=1   # increment the key value

    return history # retunn the history library 

  