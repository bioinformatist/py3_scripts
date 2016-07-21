#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = "Yu Sun"

import json
from pandas import DataFrame
from weibo import APIClient  # Sina weibo's SDK
import webbrowser  # Python's internel package

APP_KEY = '232607108'  
APP_SECRET = '69696d818e5e11f438c2f8016578c4bc'  
CALLBACK_URL = 'http://icannotendure.space/'  
  
# Use SDK for Python3.x from Internet to call API
client = APIClient(app_key=APP_KEY, app_secret=APP_SECRET, redirect_uri=CALLBACK_URL)  
# Open redirect page using default webbrowser
webbrowser.open_new(client.get_authorize_url())


# Get token access via user's input value
r = client.request_access_token(input("Input code:"))  
# Set token  
client.set_access_token(r.access_token, r.expires_in)

# Get data & statistics
friends_info = json.loads(json.dumps(client.get.friendships__friends(screen_name='我大鱼人教你当大人')['users']))
frame = DataFrame(friends_info)
print(frame['location'].str.split('\s+').str[0].value_counts())
