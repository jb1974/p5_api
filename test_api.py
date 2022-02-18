# -*- coding: utf-8 -*-
"""
Created on Thu Feb 17 11:29:11 2022

@author: james
"""

import requests
import json

#url = 'http://127.0.0.1:8000/predict'
url = 'https://ancient-tor-34149.herokuapp.com/predict'

question = json.dumps({
    'text': 'strange c error code min max call strange error c min max call visual c compiler'
    })

headers = {
    'Content-Type': 'application/json'
    }

response = requests.post(url=url, data=question, headers=headers)


print(response.text)