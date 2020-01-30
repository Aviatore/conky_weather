import urllib.request
from html.parser import HTMLParser
import re


class Parser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.data = {}
        self.day = ""
        self.c = 0

    def pr(self):
        for key in self.data.keys():
            print(key, self.data[key])

    def handle_starttag(self, tag, attrs):
        if tag == "div":
            for atr in attrs:
                if atr[1] in ["day1", "day2", "day3"]:
                    self.day = atr[1]
                    self.c = 1

        if tag == "img":
            for atr in attrs:
                if atr[1] == "weather_pictogram": self.c = 1
                if self.c == 1 and atr[0] == "title":
                    self.data[self.day] = atr[1]
                    self.c = 0


class AGHParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.data = {}
        self.parameters = ["Temperatura powietrza", "Ciśnienie atmosferyczne", "Prędkość wiatru", "pm 10"]
        self.grabParameter = 0
        self.grabValue = 0
        self.tmp = ["", 0, ""]

    def handle_starttag(self, tag, attrs):
        if tag == "td":
            self.grabParameter = 1
        elif tag == "span" and self.tmp[0] != "" and self.tmp[1] < 2:
            self.tmp[1] += 1
            if self.tmp[1] == 2:
                self.grabValue = 1
            


    def handle_data(self, data):
        if self.grabParameter and data in self.parameters:
            self.tmp[0] = data
            self.grabParameter = 0
        elif self.grabValue:
            self.tmp[2] = data.rstrip()
            self.grabValue = 0
            self.grabParameter = 0
            r = re.compile(r'\s')
            
            tmp = r.split(self.tmp[2])
            if tmp[-1] != "°C":
                self.tmp[2] = tmp[0] + " " + tmp[-1]
            else:
                self.tmp[2] = tmp[0] + tmp[-1]

            if self.tmp[0] == "pm 10":
                self.tmp[2] += '3'

            self.data[self.tmp[0]] = self.tmp[2]

#            print("DEBUG", self.tmp[2], self.tmp[0])
            self.tmp = ["", 0, ""]



url_agh = "http://meteo.ftj.agh.edu.pl/main"
url = "https://www.meteoblue.com/pl/pogoda/tydzie%C5%84/krak%C3%B3w_polska_3094802"

p = AGHParser()

resp = urllib.request.urlopen(url_agh)
outputRaw = resp.read().decode('utf-8')

p.feed(outputRaw)
print(p.data["pm 10"])