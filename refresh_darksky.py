#!/usr/bin/env python3
import json
import sys
import datetime

from datetime    import datetime
from http.client import HTTPSConnection
from pprint      import pprint
from statistics  import mean

start    = datetime.now().strftime('%Y%m%d%H%M%S')
report   = False
publish  = False
rotate   = False
forecast = {}

config = {
  'key':'e651fd6cb0ba73daaf9cab6b6c643257',
  'cities':{
    'sf':{
      'name':'Central SF',
      'lat':37.7337,
      'lon':-122.4467,
    },
    'yolo':{
      'name':'Potrero Hill',
      'lat':37.4526,
      'lon':-122.2359
    },
    'nope':{
      'name':'Outer Richmond',
      'lat':37.7780,
      'lon':-122.5004
    },
    'oakland':{
      'name':'The O',
      'lat':37.8043,
      'lon':-122.2711
    },
  }
}

try:
  if sys.argv[1] == '--report':
    report = True
  elif sys.argv[1] == '--publish':
    publish = True
  elif sys.argv[1] == '--rotate':
    print('TBD')
    quit()
  else:
    quit()
except:
  print("Usage: %s [--report|--publish|--rotate]\n" % sys.argv[0])
  quit()

for city in list(config['cities'].keys()):
  forecast[city] = {
    'temp':float(),
    'feels_like':float(),
    'avg':float(),
  }
  uri = "/forecast/%s/%0.4f,%0.4f" % ( config['key'], config['cities'][city]['lat'], config['cities'][city]['lon'] )

  conn = HTTPSConnection("api.darksky.net")
  conn.request("GET",uri)
  resp = conn.getresponse()
  bytes=resp.read()
  data=bytes.decode('utf-8')

  try:
    if int(resp.status) == 200:
      try:
        ds_json = json.loads(data)
      except:
        print('ERROR: Unparseable JSON')
        pprint(data)
        quit()

      if int(ds_json['currently']['temperature']) > 0:
        f = open('%s.json' % city,'w')
        json.dump(data,f)
        f.close()

        forecast[city]['temp'] = round(ds_json['currently']['temperature'],2)
        forecast[city]['feels_like'] = round(ds_json['currently']['apparentTemperature'],2)
        forecast[city]['avg'] = round(mean([
          ds_json['daily']['data'][0]['temperatureLow'],
          ds_json['daily']['data'][0]['temperatureHigh'],
        ]),2)
      else:
        print('ERROR: Incorrect JSON')
        pprint(ds_json['currently'])
    else:
      print('Bad Response: %i' % resp.status())
  finally:
    conn.close()

# Cherrypick the hell out of it. ( * SNRK* )
lies       = [int(forecast['sf']['temp']),int(forecast['sf']['feels_like']),int(forecast['sf']['avg'])]
damn_lies  = [int(forecast['nope']['temp']),int(forecast['nope']['feels_like']),int(forecast['nope']['avg'])]
statistics = sorted(lies + damn_lies)
zero_blind_study = sorted([int(forecast['oakland']['temp']) + 1,int(forecast['oakland']['feels_like']) + 1,int(forecast['oakland']['avg'] + 1)])

# Display data
forecast['min'] = statistics[0]
forecast['max'] = zero_blind_study[0]

# Diagnostic data
forecast['start'] = start
forecast['end']   = datetime.now().strftime('%Y%m%d%H%M%S')

# Still trying to figure out the data weirdness, specifically: "Season variation, or climate/micro-climate change?".
# Adding Potrero Hill for context, as the weirdest part is how relatively warm the Outer Richmond is/was.

if publish:
  f = open('fuckyeahhistoricaldata.json','a')
  json.dump(forecast,f)
  f.write("\n")
  f.close()
  #if rotate:
  #  # Am I sure I don't want to just stick to logrotate.d???
# TBD: --report should parse *this* file and actually contextualize some shit.


if forecast['min'] > forecast['max']:
  report  = True
  publish = False

if report:
  pprint(forecast, indent=1)

if publish:
  f = open('fuckyeahoakland.json','w')
  json.dump(forecast,f)
  f.close()

if rotate:
  print("TBD")
  quit()



