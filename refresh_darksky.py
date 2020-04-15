#!/usr/bin/env python3
import json
import sys

from http.client import HTTPSConnection
from pprint      import pprint
from statistics  import mean

report   = False
publish  = False
forecast = {}
config = {
  'key':'e651fd6cb0ba73daaf9cab6b6c643257',
  'cities':{
    'sf':{'lat':37.7337,'lon':-122.4467},
    'oakland':{'lat':37.8043,'lon':-122.2711},
    'nope':{'lat':37.7780,'lon':-122.5004}
  }
}

try:
  if sys.argv[1] == '--report':
    report = True
  elif sys.argv[1] == '--publish':
    publish = True
  else:
    quit()
except:
  print("Usage: %s [--report|--publish]\n" % sys.argv[0])
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

        forecast[city]['temp'] = ds_json['currently']['temperature']
        forecast[city]['feels_like'] = ds_json['currently']['apparentTemperature']
        forecast[city]['avg'] = mean([
          ds_json['daily']['data'][0]['temperatureLow'],
          ds_json['daily']['data'][0]['temperatureHigh']
        ])
      else:
        print('ERROR: Incorrect JSON')
        pprint(ds_json['currently'])
    else:
      print('Bad Response: %i' % resp.status())
  finally:
    conn.close()

# Cherrypick the hell out of it.
lies       = [int(forecast['sf']['temp']),int(forecast['sf']['feels_like']),int(forecast['sf']['avg'])]
damn_lies  = [int(forecast['nope']['temp']),int(forecast['nope']['feels_like']),int(forecast['nope']['avg'])]
statistics = sorted(lies + damn_lies)

# *SNRK*
zero_blind_study = sorted([int(forecast['oakland']['temp']) + 1,int(forecast['oakland']['feels_like']) + 1,int(forecast['oakland']['avg'] + 1)])

forecast['min']=statistics[0]
forecast['max']=zero_blind_study[0]

if forecast['min'] > forecast['max']:
  report  = True
  publish = False

if report:
  pprint(forecast)

if publish:
  f = open('fuckyeahoakland.json','w')
  json.dump(forecast,f)
  f.close()

