#!/usr/bin/env python3
import json
import getopt
import sys

from pprint import pprint

temp=dict()
phrase=str()
comment=str()

try:
  f = open('fuckyeahoakland.json','r')
  temp = json.load(f)
  f.close()
except IOError:
  e = sys.exc_info()[0]
  phrase = "I sincerely have no idea where my data is, but technically my SLA is 'Whenever I f*cking feel like it'"
  comment = "Where's my fucking file? %s" % e
except:
  e = sys.exc_info()[0]
  phrase = "I sincerely have no idea what's going on, but technically my SLA is 'Whenever I f*cking feel like it'."
  comment = "WTF? %s" % e

try:
  diff=round(temp['oakland']) - int(temp['sf'])
  if diff < 1:
    diff=round(temp['oakland']) - int(temp['nope']) 
except KeyError:
  diff = 0

if diff >= 1:
  phrase = "You'd be %u degrees warmer if you were in Oakland right now." % abs(diff)
else:
  phrase = "Either Oakland is abnormally chilly, or I broke the app. It's probably the latter."

content='''
<html xmlns="http://www.w3.org/1999/xhtml">
  <head>
    <meta http-equiv="Content-Type" content="text/html; charset=UTF-8"/>
    <title>FUCK YEAH OAKLAND</title><meta name="description" content=""/>
    <style type="text/css">
        @import url("fuckyeah.css");
    </style>
  </head>
  <body>
  <h1>%s</h1>

  <!--
    Oakland:		%f
    Central SF:		%f
    Outer Richmond:	%f
    %s
  -->

  <h3>
    [<a href="http://darksky.net/poweredby/"><img src="./static/poweredby-oneline.png"></a>]
  </h3>
  <h4>
    [...AND <a href="http://maps.google.com/maps/ms?ie=UTF8&hl=en&msa=0&msid=111386974984487942660.00043b9b4dc191c072885&om=0&ll=37.784554,-122.23526&spn=0.086556,0.194664&z=12">TACOS</a>]
  </h4>
  </body>
</html>
'''

print(content % (phrase,temp['oakland'],temp['sf'],temp['nope'],comment) )

