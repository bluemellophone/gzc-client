#!/usr/bin/env python

import json
import string
import random
import requests
from os import listdir
from os.path import join


alphabet = string.ascii_lowercase


def get_data(color, number, person):
    data = {
        'car_color': color,
        'car_number': number,
        'person_letter': person,
        'image_first_time_hour': random.randint(0, 23),
        'image_first_time_minute': random.randint(0, 59),
    }
    return data


test_dir = 'stress_test'
test_archives = [f for f in listdir(test_dir) if f.endswith('.zip')]

cars = [('BLUE', 1, (alphabet[x] for x in range(0, 6))), ('RED', 2, (alphabet[x] for x in range(0, 6))), ('GREEN', 3, (alphabet[x] for x in range(0, 6)))]
pairs = [random.choice(cars) for _ in test_archives]
colors = [x[0] for x in pairs]
numbers = [x[1] for x in pairs]
persons = [x[2].next() for x in pairs]

DOMAIN = 'http://localhost:5000'
IMGURL = DOMAIN + '/images/submit'
GPSURL = DOMAIN + '/gps/submit'


for test_archive, color, number, person in zip(test_archives, colors, numbers, persons):
    content = open(join(test_dir, test_archive), 'rb')
    files = {'image_archive': content}
    data = get_data(color, number, person)
    print data
    r = requests.post(IMGURL, data=data, files=files)
    print("HTTP STATUS:", r.status_code)
    response = json.loads(r.text)
    print("RESPONSE:", response)
