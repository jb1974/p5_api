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
    'text': 'How di I merge 2 different columns of a dataframe using pandas in python?'
    })

headers = {
    'Content-Type': 'application/json'
    }

response = requests.post(url=url, data=question, headers=headers)


print(response.text)