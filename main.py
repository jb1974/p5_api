# -*- coding: utf-8 -*-
"""
Created on Wed Feb  9 14:09:36 2022

@author: james
"""
# #############################################################################
# 1. Library imports
# #############################################################################

## preprocessing
import re
import nltk
import spacy
from bs4 import BeautifulSoup
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer

## misc
import joblib

## api
import uvicorn
from fastapi import FastAPI
from pydantic import BaseModel

# #############################################################################
# 2. Create app and model objects
# #############################################################################
app = FastAPI()

class Question(BaseModel):
    text: str

# Tokenisation
tokenizer = nltk.RegexpTokenizer(r'\w+')

# Stopwords deletion
all_stopwords = stopwords.words('english')

# Lemmatization
lemmatizer = WordNetLemmatizer()

# Delete numbers
r = re.compile(".*[a-zA-Z]")

# Delete verbs with Part of speech (POS)
pos = spacy.load("en_core_web_sm")

def preprocessing(text):
    # HTML cleaning
    text = BeautifulSoup(text, 'html.parser').get_text()

    # Remove punctuation
    text = re.sub('[,\.!?\_\-\*(){}/]', '', text)

    # Convert to lowercase
    text = text.lower()

    # Tokenisation
    text = tokenizer.tokenize(text)

    # Stopwords deletion
    text = [word for word in text
            if not word in all_stopwords]

    # Lemmatization
    result = []
    for word in text:
        result.append(lemmatizer.lemmatize(word))
    text = result

    # Delete numbers
    text = list(filter(r.match, text))
    
    # Delete verbs
    result = []
    doc = pos(' '.join(text))
    for token in doc:
        if token.pos_ != 'VERB':
            result.append(token.text)
    text = result

    return text

# MultiLabelBinarizer
mlb = joblib.load('mlb.jl')

# Model
model = joblib.load('tfidf.jl')

# #############################################################################
# 3. Index route, opens automatically on http://127.0.0.1:8000
# #############################################################################
@app.get('/')
def index():
    return {'message': 'ML API: delivers tags from input question'}

# #############################################################################
# 4. Expose the prediction functionality, make a prediction from the passed
#    JSON data and return the tags
# #############################################################################
@app.post('/predict')
def predict_tags(Q: Question):
    # preprocessing
    temp = preprocessing(Q.text)
    
    # format
    question = ''
    for word in temp:
        question += ' ' + word
    
    # make prediction using model
    prediction = model.predict([question]) 

    return mlb.inverse_transform(prediction)

if __name__ == '__main__':

    uvicorn.run(app, host='127.0.0.1', port=8000, debug=True)