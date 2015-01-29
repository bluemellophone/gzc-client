from __future__ import absolute_import, division, print_function
import requests
import simplejson as json

# This is test code for pushing POST content and a zip file to a web server.
# Run server.py from https://github.com/bluemellophone/gzc-server and then run this
# client.

DOMAIN = 'http://localhost:5000'
URL = DOMAIN + '/images/submit'

# LOAD THE POST VARIABLES
data = {
    'car_color': 'RED',
    'car_number': 1,
    'person_letter': 'A',
    'image_first_time_hour': 10,
    'image_first_time_minute': 36,
}

# LOAD THE ZIP AND ADD TO THE PAYLOAD
content = open('test.zip', 'rb')
files = {
    'image_archive': content,
}

# SEND POST REQUEST WITH data AND files PAYLOADS
r = requests.post(URL, data=data, files=files)

# Response
print("HTTP STATUS:", r.status_code)
response = json.loads(r.text)
print("RESPONSE:", response)
