#!/usr/bin/python
# -*- coding: utf-8 -*-

# Getting weather forecast from worldweatheronline.com

import sys
import os
import datetime
import json
import urllib2

################################### Settings ###################################

# set path of the cache-file
cache_file_path = '/home/bery/conky/cache/weather'

# set worldweatheronline.com KEY
wwo_key = 'set-your-key'  # for example '1111111111111111111111'

# set location query by examples http://www.worldweatheronline.com/weather-api.aspx
wwo_location = 'set-your-location'  # for example 'Decin, Czech Republic'

# set number of days you wanna get (for the template)
wwo_num_of_days = 3

# set template
template = u'''${image %(TODAY_IMAGE)s -p 0,645 -s 90x90}${voffset 7}${offset 105}${font Bitstream Vera Sans Mono:style=Bold:size=20}${color2}%(TODAY_TEMP)s °C${color}${font}

${goto 105}Observation time:          ${color2}%(TODAY_OBSERVATION)s ${color}
Wind speed:                  ${color2}%(TODAY_WINDSPEED)s km/h ${color}
Humidity:                      ${color2}%(TODAY_HUMIDITY)s %% ${color}


      %(1_DATE)s                    %(2_DATE)s                    %(3_DATE)s
${voffset 5}${goto 60}${font Bitstream Vera Sans Mono:style=Bold:size=12}${color2}%(1_TEMP)s °C${font}${font :size=8}
%(1_WINDSPEED)s km/h${color}${font}${voffset -37}${goto 208}${color2}${font Bitstream Vera Sans Mono:style=Bold:size=12}
%(2_TEMP)s °C${font}${font :size=8}
%(2_WINDSPEED)s km/h${color}${font}${voffset -37}${goto 358}${color2}${font Bitstream Vera Sans Mono:style=Bold:size=12}
%(3_TEMP)s °C${font}${font :size=8}
%(3_WINDSPEED)s km/h${color}${font}
${image %(1_IMAGE)s -p 0,775 -s 45x45}${image %(2_IMAGE)s -p 150,775 -s 45x45}${image %(3_IMAGE)s -p 300,775 -s 45x45}'''

#################################### Script ####################################

def getUrlData(url, x=0):
  """load data from url recursively"""
  try:
    uo = urllib2.urlopen(url)
    text = uo.read()
    if text:
      return text
  except:
    pass

  if x == 4:
    sys.exit(0)
  time.sleep(5)
  return getUrlData(url, x+1)


url = 'http://api.worldweatheronline.com/free/v1/weather.ashx?q=%s&format=json&num_of_days=%s&key=%s' % (urllib2.quote(wwo_location), wwo_num_of_days, wwo_key)

try:
  jstr = getUrlData(url)
  jdata = json.loads(jstr, encoding='utf-8')
except:
  sys.exit(0)

if 'data' not in jdata:
  sys.exit(0)
elif not jdata['data'].get('current_condition'):
  sys.exit(0)

icons_path = '$HOME/conky/weather-icons/'

repl = {}

# data.current_condition
cc = jdata['data']['current_condition'][0]
try:
  img_name = cc['weatherIconUrl'][0]['value']
  img_name = os.path.basename(img_name)
except:
  img_name = 'na.png'
repl['TODAY_IMAGE'] = os.path.join(icons_path, img_name)
repl['TODAY_TEMP'] = cc.get('temp_C', '?')
if cc.get('observation_time'):
  repl['TODAY_OBSERVATION'] = datetime.datetime.strptime(cc['observation_time'], '%I:%M %p').strftime('%H:%M')
else:
  repl['TODAY_OBSERVATION'] = 'unknown'
repl['TODAY_WINDSPEED'] =  cc.get('windspeedKmph', '?')
repl['TODAY_HUMIDITY'] = cc.get('humidity', '?')

# data.weather - list
x = 1
for i in jdata['data'].get('weather', []):
  try:
    img_name = i['weatherIconUrl'][0]['value']
    img_name = os.path.basename(img_name)
  except:
    img_name = 'na.png'
  repl['%s_IMAGE' % x] = os.path.join(icons_path, img_name)
  repl['%s_TEMP' % x] = '%s/%s' % (i.get('tempMinC', '?'), i.get('tempMaxC', '?'))
  repl['%s_DATE' % x] = datetime.datetime.strptime(i['date'], '%Y-%m-%d').strftime('%a %d.%m.')
  repl['%s_WINDSPEED' % x] = i.get('windspeedKmph', '?')
  x += 1

data = template % repl

# write into a cache-file
try:
  f = open(cache_file_path, 'w')
  f.write(data.encode('utf-8'))
  f.close()
except:
  pass

sys.exit()