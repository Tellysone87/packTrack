from flask import make_response
from functools import wraps, update_wrapper
from datetime import datetime


# This code was found online at https://arusahni.net/blog/2014/03/flask-nocache.html.
# I did not write or own this code in anyway. It was used to help me secure the members
# profile after logging out. In chrome and fire fox you were able to use the back button
# and get back into the signed out users profile. I did try researching solutions but wher not able to find any.
# I will researh this function to be sure I understand hoe it works. 

def nocache(view):
    @wraps(view) #sets the decorater to the page and sets the following headers
    def no_cache(*args, **kwargs):
        response = make_response(view(*args, **kwargs))
        response.headers['Last-Modified'] = datetime.now()
        response.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate, post-check=0, pre-check=0, max-age=0'
        response.headers['Pragma'] = 'no-cache'
        response.headers['Expires'] = '-1'
        return response
        
    return update_wrapper(no_cache, view)