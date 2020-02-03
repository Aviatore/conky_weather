import urllib.request
from html.parser import HTMLParser
import re
import json


class AGHParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.data = {}
        self.parameters = ["Temperatura powietrza", "Ciśnienie atmosferyczne", "Prędkość wiatru", "pm 10"]
        self.grabValue = 0
        self.tmp = ["", 0, ""] # [0] - nazwa parametru, [1] - liczba wystąpień tagu <span>, [2] - wartość parametru

    def handle_starttag(self, tag, attrs):
        if tag == "span" and self.tmp[0] != "" and self.tmp[1] < 2:
            self.tmp[1] += 1
            if self.tmp[1] == 2:
                self.grabValue = 1

    def handle_data(self, data):
        if data in self.parameters:
            self.tmp[0] = data
        elif self.grabValue:
            self.tmp[2] = data.rstrip()
            self.grabValue = 0
            r = re.compile(r'\s')
            
            tmp = r.split(self.tmp[2])
            if tmp[-1] != "°C":
                self.tmp[2] = tmp[0] + " " + tmp[-1]
            else:
                self.tmp[2] = tmp[0] + tmp[-1]

            if self.tmp[0] == "pm 10":
                self.tmp[2] += '3'

            self.data[self.tmp[0]] = self.tmp[2]

            self.tmp = ["", 0, ""]



class Weather():
    def __init__(self, url):
        self.url = url
        self.data = {}
    
    def parse(self):
        with open("data.json", 'r') as f:
            data = f.read()
        
        dataDict = json.loads(data)
        
        self.data["currDesc"] = dataDict["list"][0]["weather"][0]["description"]
        self.data["currIcon"] = dataDict["list"][0]["weather"][0]["icon"]
        self.data["currDate"] = [d for d in dataDict["list"][0]["dt_txt"].split(" ")]

        for t in dataDict["list"]:
            if t["dt_txt"].split(" ")[0] == self.data["currDate"][0] and t["dt_txt"].split(" ")[1] == "00:00:00":
                self.data["currNightDesc"] = t["weather"][0]["description"]
                self.data["currNightIcon"] = t["weather"][0]["icon"]
                self.data["currNightDate"] = [d for f in t["weather"][0]["dt_txt"].split(" ")]


url_agh = "http://meteo.ftj.agh.edu.pl/main"

agh = AGHParser()

agh_resp = urllib.request.urlopen(url_agh)
agh_outputRaw = agh_resp.read().decode('utf-8')

agh.feed(agh_outputRaw)
print(agh.data["pm 10"])