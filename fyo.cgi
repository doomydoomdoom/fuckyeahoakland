#!/usr/bin/env python3
import json
import sys

forecast=dict()
phrase=str()
comment=str('Insert easter egg here: X')
diff=int(0)

# Display-side error handling
try:
  f = open('fuckyeahoakland.json','r')
  forecast = json.load(f)
  f.close()
except IOError:
  comment = "WTF? %s" % sys.exc_info()[0]
except:
  comment = "WTF? %s" % sys.exc_info()[0]

# Validation moved to cron, but we still need to fail gracefully.
try:
  diff=round(forecast['max']) - int(forecast['min'])
except:
  diff = 0
# ...and if you can't faily gracefully, sarcastically candid works! ( YOLO )

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

print(content % (phrase,comment))

