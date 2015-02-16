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

##########################################################################################
##########################################################################################
##########################################################################################

# LOAD THE POST VARIABLES
data = {
    'car_color': 'RED',
    'car_number': 1,
    'person_letter': 'A',
    'image_first_time_hour': 10,
    'image_first_time_minute': 36,
}

# LOAD THE ZIP FILE AND ADD TO THE PAYLOAD
content = open('test_image.zip', 'rb')
files = {
    'image_archive': content,
}

# SEND POST REQUEST WITH data AND files PAYLOADS
r = requests.post(IMGURL, data=data, files=files)

# RESPONSE
print("HTTP STATUS:", r.status_code)
response = json.loads(r.text)
print("RESPONSE:", response)

##########################################################################################
##########################################################################################
##########################################################################################

# LOAD THE POST VARIABLES
data = {
    'car_color': 'RED',
    'car_number': 1,
    'gps_first_time_hour': 10,
    'gps_first_time_minute': 03,
}

# LOAD THE GPX FILE AND ADD TO THE PAYLOAD
content = open(join('test_gps', 'track.gpx'), 'rb')
files = {
    'gps_data': content,
}

# SEND POST REQUEST WITH data AND files PAYLOADS
r = requests.post(GPSURL, data=data, files=files)

# RESPONSE
print("HTTP STATUS:", r.status_code)
response = json.loads(r.text)
print("RESPONSE:", response)
