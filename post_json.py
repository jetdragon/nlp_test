import requests
import json

data = open('newsSet.json', 'rb').read()

url = 'http://127.0.0.1:5000/nlp/sentiment'
headers = {'Content-Type' : 'application/json'}
r = requests.post(url, data, headers=headers)
