import urllib.request
from html.parser import HTMLParser
import re
import json
import datetime as d
import time


class AGHParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.data = {}
        self.parameters = ["Temperatura powietrza", "Ciśnienie atmosferyczne", "Prędkość wiatru", "pm 10"]
        self.grabValue = 0
        self.timeTmp = [0, 0]
        self.tmp = ["", 0, ""] # [0] - nazwa parametru, [1] - liczba wystąpień tagu <span>, [2] - wartość parametru

    def handle_starttag(self, tag, attrs):
        if tag == "span" and self.tmp[0] != "" and self.tmp[1] < 2:
            self.tmp[1] += 1
            if self.tmp[1] == 2:
                self.grabValue = 1

        if len(attrs) > 0:
            if self.timeTmp[0] == 1 and attrs[0][0] == "class" and attrs[0][1] == "important":
                self.timeTmp[1] = 1

    def handle_data(self, data):
        r = re.compile(r'\s')

        if data in self.parameters:
            self.tmp[0] = data
        elif "Data ostatniego pomiaru" in data:
            self.timeTmp[0] = 1
        elif self.timeTmp[1] == 1:
            tmp = r.split(data.rstrip())
            self.data["time"] = ":".join(tmp[-1].split(":")[0:2])
            self.timeTmp = [0, 0]
        elif self.grabValue:
            self.tmp[2] = data.rstrip()
            self.grabValue = 0
            
            tmp = r.split(self.tmp[2])
            if tmp[-1] != "°C":
                self.tmp[2] = tmp[0] + " " + tmp[-1]
            else:
                self.tmp[2] = tmp[0] + tmp[-1]

            if self.tmp[0] == "pm 10":
                self.tmp[2] += '3'

            self.data[self.tmp[0]] = self.tmp[2]

            self.tmp = ["", 0, ""]


class Weather:
    def __init__(self, urlForecast, urlWeather):
        self.urlForecast = urlForecast
        self.urlWeather = urlWeather
        self.data = {}

    def nextDay(self, n):
        return (d.date.fromisoformat(self.data["currDate"]) + d.timedelta(days=n)).strftime("%Y-%m-%d")

    def formatDate(self, dateStr):
        date = d.date.fromisoformat(dateStr)
        return date.strftime("%a %d.%m")

    def chooseIcon(self, description, icon):
        if description == "całkowite zachmurzenie":
            return "04_2" + icon[-1]
        elif "04" in icon:
            return "04_1" + icon[-1]
        else:
            return icon

    def parse(self):
        print("Getting openweathermap Weather json ...")
#        with open("data.json", 'r') as f:
#            data = f.read()

        resp = urllib.request.urlopen(self.urlWeather)
        data = resp.read().decode('utf-8')

        print("Parsing Weather json file ...")
        dataDict = json.loads(data)

        self.data["currDesc"] = dataDict["weather"][0]["description"]
        self.data["currIcon"] = dataDict["weather"][0]["icon"]
        self.data["currIcon"] = self.chooseIcon(self.data["currDesc"], self.data["currIcon"])
        self.data["currDate"] = d.date.fromtimestamp(dataDict["dt"]).strftime("%Y-%m-%d")

        print("Getting openweathermap Forecast json ...")
        resp = urllib.request.urlopen(self.urlForecast)
        data = resp.read().decode('utf-8')

        print("Parsing Forecast json file ...")
        dataDict = json.loads(data)

        for t in dataDict["list"]:
            if t["dt_txt"].split(" ")[0] == self.nextDay(1) and t["dt_txt"].split(" ")[1] == "00:00:00":
                self.data["currNightDesc"] = t["weather"][0]["description"]
                self.data["currNightIcon"] = t["weather"][0]["icon"]
                self.data["currNightIcon"] = self.chooseIcon(self.data["currNightDesc"], self.data["currNightIcon"])
                self.data["currNightDate"] = [d for d in t["dt_txt"].split(" ")]
                self.data["currNightTemp"] = str(round(t["main"]["temp"], 1)) + "°C"
                self.data["currNightWind"] = str(round(t["wind"]["speed"], 1)) + " m/s"
            if t["dt_txt"].split(" ")[0] == self.nextDay(1) and t["dt_txt"].split(" ")[1] == "12:00:00":
                self.data["nextDay1Desc"] = t["weather"][0]["description"]
                self.data["nextDay1Icon"] = t["weather"][0]["icon"]
                self.data["nextDay1Icon"] = self.chooseIcon(self.data["nextDay1Desc"], self.data["nextDay1Icon"])
                self.data["nextDay1Date"] = [d for d in t["dt_txt"].split(" ")]
                self.data["nextDay1Temp"] = str(round(t["main"]["temp"], 1)) + "°C"
                self.data["nextDay1Wind"] = str(round(t["wind"]["speed"], 1)) + " m/s"
            if t["dt_txt"].split(" ")[0] == self.nextDay(2) and t["dt_txt"].split(" ")[1] == "12:00:00":
                self.data["nextDay2Desc"] = t["weather"][0]["description"]
                self.data["nextDay2Icon"] = t["weather"][0]["icon"]
                self.data["nextDay2Icon"] = self.chooseIcon(self.data["nextDay2Desc"], self.data["nextDay2Icon"])
                self.data["nextDay2Date"] = [d for d in t["dt_txt"].split(" ")]
                self.data["nextDay2Temp"] = str(round(t["main"]["temp"], 1)) + "°C"
                self.data["nextDay2Wind"] = str(round(t["wind"]["speed"], 1)) + " m/s"
            if t["dt_txt"].split(" ")[0] == self.nextDay(3) and t["dt_txt"].split(" ")[1] == "12:00:00":
                self.data["nextDay3Desc"] = t["weather"][0]["description"]
                self.data["nextDay3Icon"] = t["weather"][0]["icon"]
                self.data["nextDay3Icon"] = self.chooseIcon(self.data["nextDay3Desc"], self.data["nextDay3Icon"])
                self.data["nextDay3Date"] = [d for d in t["dt_txt"].split(" ")]
                self.data["nextDay3Temp"] = str(round(t["main"]["temp"], 1)) + "°C"
                self.data["nextDay3Wind"] = str(round(t["wind"]["speed"], 1)) + " m/s"

def getAGHData():
    url_agh = "http://meteo.ftj.agh.edu.pl/main"
    print("Getting AGH webpage ...")
    agh_resp = urllib.request.urlopen(url_agh)
    agh_outputRaw = agh_resp.read().decode('utf-8')
    agh = AGHParser()
    print("Parsing AGH webpage ...")
    agh.feed(agh_outputRaw)
    return agh

def getWeatherData():
    urlForecast = 'http://api.openweathermap.org/data/2.5/forecast?id=3094802&APPID=8a4f646122f8a3b175de60d3f6669c20&units=metric&lang=pl'
    urlWeather = 'http://api.openweathermap.org/data/2.5/weather?id=3094802&APPID=8a4f646122f8a3b175de60d3f6669c20&units=metric&lang=pl'
    weather = Weather(urlForecast, urlWeather)
    weather.parse()
    return weather

def setPosition(prevString, stringStdLen):
    s = 0
    arLen = len(prevString)
    for i in prevString:
        s += len(i)
    return (s - (arLen * stringStdLen)) * 7 # 7 - szerokość pojedynczego znaku w pikselach; 5 - liczba znaków dla referencyjnej temp., np. 1.2°C

def printOutput(agh, weather):
    print("Printing weather.txt file ...")
    outputString = """
${{image icons/new/Images/new/{}.png -p 5,50 -s 140x96}}
${{color gray}}${{font DejaVu Sans Mono:size=9}}${{offset 155}}Temperatura: ${{color orange}}{}
${{color gray}}${{font DejaVu Sans Mono:size=9}}${{offset 155}}Ciśnienie: ${{color orange}}{}
${{color gray}}${{font DejaVu Sans Mono:size=9}}${{offset 155}}Prędkość wiatru: ${{color orange}}{}${{goto 0}}${{alignr 24}}${{font DejaVu Sans Mono:size=9}}{}
${{color gray}}${{font DejaVu Sans Mono:size=9}}${{offset 155}}pm10: ${{color orange}}{}${{goto 0}}${{alignr 10}}${{font DejaVu Sans Mono:size=9}}{}
${{color gray}}${{font DejaVu Sans Mono:size=9}}${{offset 155}}Czas pomiaru: ${{color orange}}{}
${{color gray}}${{font DejaVu Sans Mono:size=9}}${{offset 5}}${{voffset 5}}{}${{goto 0}}${{offset 380}}${{font DejaVu Sans Mono:size=7}}{}
${{image icons/new/Images/new/{}.png -p 340,80 -s 87x60}}
${{goto 0}}${{color gray}}${{font DejaVu Sans Mono:size=9}}${{offset 100}}${{voffset 25}}{}${{goto 0}}${{offset 260}}{}${{goto 0}}${{offset 410}}{}
${{alignr {}}}${{voffset 15}}${{color orange}}${{font DejaVu Sans Mono:size=9}}{}${{alignr {}}}{}${{alignr 24}}{}
${{alignr {}}}${{color orange}}${{font DejaVu Sans Mono:size=9}}{}${{alignr {}}}{}${{alignr 9}}{}
${{goto 0}}${{color gray}}${{font DejaVu Sans Mono:size=7}}${{offset 60}}${{voffset 25}}{}${{goto 0}}${{offset 220}}{}${{goto 0}}${{offset 380}}{}

${{image icons/new/Images/new/{}.png -p 5,220 -s 87x60}}
${{image icons/new/Images/new/{}.png -p 170,220 -s 87x60}}
${{image icons/new/Images/new/{}.png -p 340,220 -s 87x60}}
""".format(weather.data["currIcon"],
           agh.data["Temperatura powietrza"],
           agh.data["Ciśnienie atmosferyczne"],
           agh.data["Prędkość wiatru"],
           weather.data["currNightTemp"],
           agh.data["pm 10"],
           weather.data["currNightWind"],
           agh.data["time"],
           weather.data["currDesc"],
           weather.data["currNightDesc"],
           weather.data["currNightIcon"],
           weather.formatDate(weather.data["nextDay1Date"][0]),
           weather.formatDate(weather.data["nextDay2Date"][0]),
           weather.formatDate(weather.data["nextDay3Date"][0]),
           283 + setPosition([weather.data["nextDay2Temp"], weather.data["nextDay3Temp"]], 5),
           weather.data["nextDay1Temp"],
           153 + setPosition([weather.data["nextDay3Temp"]], 5),
           weather.data["nextDay2Temp"],
           weather.data["nextDay3Temp"],
           227 + setPosition([weather.data["nextDay2Wind"], weather.data["nextDay3Wind"]], 7),
           weather.data["nextDay1Wind"],
           125 + setPosition([weather.data["nextDay3Wind"]], 7),
           weather.data["nextDay2Wind"],
           weather.data["nextDay3Wind"],
           weather.data["nextDay1Desc"],
           weather.data["nextDay2Desc"],
           weather.data["nextDay3Desc"],
           weather.data["nextDay1Icon"],
           weather.data["nextDay2Icon"],
           weather.data["nextDay3Icon"]
           )

    with open("weather.txt", 'w') as f:
        f.write(outputString)


def main():
    weather = getWeatherData()
    weather_counter_tmp = time.time()
    while True:
        t = time.time()
        if (t - weather_counter_tmp) >= 3600:
            weather = getWeatherData()
            weather_counter_tmp = t
        agh = getAGHData()
        printOutput(agh, weather)
        time.sleep(300)


if __name__ == '__main__':
    main()
#print(outputString)
