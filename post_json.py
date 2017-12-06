import requests
import json

data = open('newsSet.json', 'rb').read()

url = 'http://127.0.0.1:5000/nlp/sentiment'
headers = {'Content-Type' : 'application/json'}
r = requests.post(url, data, headers=headers)

# result = json.loads(r.content)
# result_str = json.dumps(result)
# result_file = "result.json"
# with open(result_file, "w") as f :
#     f.write(result_str)
print(json.loads(r.content))
