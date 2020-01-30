import urllib.request
from html.parser import HTMLParser


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
                if atr[1] == "weather_pictogram": c = 1
                if self.c == 1 and atr[0] == "title":
                    self.data[self.day] = atr[1]
                    self.c = 0


class AGHParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.data = {}
        self.parameters = ["Temperatura powietrza", "Ciśnienie atmosferyczne", "Prędkość wiatru", "pm 10"]
        self.grabPrameter = 0
        self.grabValue = 0
        self.tmp = []

    def handle_starttag(self, tag, attrs):
        if tag == "td":
            self.grabParameter = 1
        elif tag == "span"

    def handle_data(self, data):
        if self.grabParameter and data in self.parameters:
            self.tmp.append(data)
        elif self.grabValue and self


url_agh = "http://meteo.ftj.agh.edu.pl/main"
url = "https://www.meteoblue.com/pl/pogoda/tydzie%C5%84/krak%C3%B3w_polska_3094802"

p = Parser()

resp = urllib.request.urlopen(url)
outputRaw = resp.read().decode('utf-8')

p.feed(outputRaw)
p.pr()