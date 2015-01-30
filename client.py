#!/usr/bin/env python
from __future__ import absolute_import, division, print_function
import requests
import simplejson as json
from os.path import join, exists  # NOQA

# This is test code for pushing POST content and a zip file to a web server.
# Run server.py from https://github.com/bluemellophone/gzc-server and then run this
# client.

DOMAIN = 'http://localhost:5000'
IMGURL = DOMAIN + '/images/submit'
GPSURL = DOMAIN + '/gps/submit'

# LOAD THE POST VARIABLES
data = {
    'car_color': 'RED',
    'car_number': 1,
    'person_letter': 'A',
    'image_first_time_hour': 10,
    'image_first_time_minute': 36,
}

# image data
# LOAD THE ZIP AND ADD TO THE PAYLOAD
content = open('test.zip', 'rb')
files = {
    'image_archive': content,
}

# SEND POST REQUEST WITH data AND files PAYLOADS
r = requests.post(IMGURL, data=data, files=files)

# Response
print("HTTP STATUS:", r.status_code)
response = json.loads(r.text)
print("RESPONSE:", response)

# gps data
content = open(join('dummy_gps', 'dummy_gps.csv'), 'rb')
files = {
    'gps_data': content,
}

r = requests.post(GPSURL, data=data, files=files)
print("HTTP STATUS:", r.status_code)
response = json.loads(r.text)
print("RESPONSE:", response)

