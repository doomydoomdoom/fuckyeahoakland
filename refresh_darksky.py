#!/usr/bin/env python3
import json
import getopt
import sys
import http.client

from pprint import pprint

config = {
  'key':'e651fd6cb0ba73daaf9cab6b6c643257',
  'cities':{
    'sf':{'lat':37.7337,'lon':-122.4467},
    'oakland':{'lat':37.8043,'lon':-122.2711},
    'nope':{'lat':37.7780,'lon':-122.5004}
  }
}

temp = {
  'oakland':0,
  'sf':0,
  'nope':0,
}

for city in ('sf','oakland','nope'):
  uri = "/forecast/%s/%0.4f,%0.4f" % ( config['key'], config['cities'][city]['lat'], config['cities'][city]['lon'] )

  conn = http.client.HTTPSConnection("api.darksky.net")
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
        try:
          type(ds_json)
          f = open('%s.json' % city,'w')
          #f.write(data)
          json.dump(data,f)
          f.close()
          temp[city]=ds_json['currently']['temperature']
        except:
          print("ERROR:")
          e = sys.exc_info()[0]
          print(e)
          quit()
      else:
          print('ERROR: Bad JSON')
          pprint(ds_json['currently'])
          quit()
    else:
      print('Bad Response: %i' % resp.status())
      pprint(data)
      quit()
  except:
    print('Failed Response: %i' % resp.status)
    pprint(resp)
  finally:
    conn.close()

diff=round(temp['oakland']) - int(temp['sf'])
if diff < 0:
  #BLATANT CHEATING... cherry-pick the coldest micro-climate
  diff=round(temp['oakland']) - int(temp['nope'])

if diff < 0:
  print("Oakland:        %f" % temp['oakland'])
  print("Central SF:     %f" % temp['sf'])
  print("Outer Richmond: %f" % temp['nope'])
else:
  f = open('fuckyeahoakland.json','w')
  json.dump(temp,f)
  f.close()

