#!/usr/bin/env python3
import json
import getopt
import sys

from pprint import pprint

config = {
  'key':'e651fd6cb0ba73daaf9cab6b6c643257',
  'cities':{
    'sanfrancisco':{'lat':37.7337,'lon':-122.4467},
    'oakland':{'lat':37.8043,'lon':-122.2711},
    'nope':{'lat':37.7780,'lon':-122.5004}
  }
}

argv = sys.argv[1:]
opts, args = getopt.getopt(argv, 'r')

if len(list(opts)) > 0:

  import http.client
 
  for city in ('sanfrancisco','oakland','nope'):
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
          #print("SUCCESS: %s = %f" % (city,ds_json['currently']['temperature']))
          try:
            type(ds_json)
            f = open('%s.json' % city,'w')
            #f.write(data)
            json.dump(data,f)
            f.close()
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
        quit()
    finally:
      conn.close()
else:
  try:

    f = open('oakland.json','r')
    oakland = json.loads(json.load(f))
    f.close()

    f = open('sanfrancisco.json','r')
    sanfrancisco = json.loads(json.load(f))
    f.close()

    f = open('nope.json','r')
    nope = json.loads(json.load(f))
    f.close()

    # *THIS* has to be run hourly.
    diff=int(oakland['currently']['temperature']) - int(sanfrancisco['currently']['temperature'])
    delta=abs(diff)
    # To run daily, calculate an average from city['daily'][0]['temperatureM**'] and TEST THOROUGHLY.

    if diff < 0:
      #BLATANT CHEATING... cherry-pick the coldest micro-climate
      diff=int(oakland['currently']['temperature']) - int(nope['currently']['temperature'])
      delta=abs(diff)

    if diff < 0:
      phrase = "It's currently %u degrees warmer in SF, and I'm a little confused." % delta
    elif diff > 0:
      phrase = "You'd be %u degrees warmer if you were in Oakland right now." % delta
    else:
      phrase = "Either Oakland is abnormally chilly, or I broke the app. It's probably the latter."

  except IOError:
    phrase = "Where's my fucking file?"
  except:
    e = sys.exc_info()[0]
    phrase = "I sincerely have no idea what's going on, but technically my SLA is 'Whenever I f*cking feel like it', so: %s" % e

  content='''
<html xmlns="http://www.w3.org/1999/xhtml" id="foo" class="bar">
  <head>
    <meta http-equiv="Content-Type" content="text/html; charset=UTF-8"/>
    <title>FUCK YEAH OAKLAND</title><meta name="description" content=""/>
    <style type="text/css">
        @import url("fuckyeah.css");
    </style>
  </head>
  <body>
  <h1>%s</h1>
  <h3>
    [<a href="http://darksky.net/poweredby/"><img src="./static/poweredby-oneline.png"></a>]
  </h3>
  <h4>
    [...AND <a href="http://maps.google.com/maps/ms?ie=UTF8&hl=en&msa=0&msid=111386974984487942660.00043b9b4dc191c072885&om=0&ll=37.784554,-122.23526&spn=0.086556,0.194664&z=12">TACOS</a>]
  </h4>
  </body>
</html>
'''

  print(content % phrase)

