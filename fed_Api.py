from flask import Flask, render_template, request

from pprint import pformat
import os
import requests

API_KEY = os.environ['FedEx_Api_key']

url = "https://apis-sandbox.fedex.com/track/v1/trackingnumbers"
key = API_KEY

payload = {'apikey': API_KEY}
payload['trackingnumbers'] = 619945437643

headers = {
    'Content-Type': "application/json",
    'X-locale': "en_US",
    'Authorization': "Bearer"
    }

response = requests.post(url, data=payload, headers=headers)

print(response.text)