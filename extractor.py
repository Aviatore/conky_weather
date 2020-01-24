import urllib.request as r
import json

with open('data.json', 'r') as f:
    dataRaw = f.read()

data = json.loads(dataRaw)
for i in data['list']:
    print("{} : {} : {}".format(i['weather'][0]['description'], i['weather'][0]['icon'], i['dt_txt']))

