from __future__ import absolute_import, division, print_function

import subprocess
from os.path import join, exists  # NOQA
from os import mkdir
from datetime import datetime
import time
import xml.etree.ElementTree as ET


def ensure_structure(data, kind, car_number, car_color, person=None):
    data       = data.lower()
    kind       = kind.lower()
    car_number = car_number.lower()
    car_color  = car_color.lower()
    # Create data dir
    if not exists(data):
        mkdir(data)
    # Create kind dir
    kind_dir = join(data, kind)
    if not exists(kind_dir):
        mkdir(kind_dir)
    # Create car dir
    car_dir = join(kind_dir, car_number + car_color)
    if not exists(car_dir):
        mkdir(car_dir)
    # If no person, return car dir
    if person is None:
        return car_dir
    # Create person dir
    person     = person.lower()
    person_dir = join(car_dir, person)
    if not exists(person_dir):
        mkdir(person_dir)
    # Return peron dir
    return person_dir


def convert_gpx_to_json(gpx_str):
    json_list = []
    root = ET.fromstring(gpx_str)
    #try:
    #    root = ET.fromstring(gpx_str)
    #except ET.ParseError:
    #    print "Couldn't parse GPX File"
    #    return { "track": [] }

    namespace = '{http://www.topografix.com/GPX/1/1}'
    # Load all waypoint elements
    element = './/%strkpt' % (namespace, )
    trkpt_list = root.findall(element)
    for trkpt in trkpt_list:
        # Load time out of trkpt
        element = './/%stime' % (namespace, )
        dt = datetime.strptime(trkpt.find(element).text, '%Y-%m-%dT%H:%M:%S.%fZ')
        # Gather values
        posix = int(time.mktime(dt.timetuple()))
        lat   = float(trkpt.get('lat'))
        lon   = float(trkpt.get('lon'))
        json_list.append({
            'time': posix,
            'lat':  lat,
            'lon':  lon,
        })
    return { "track": json_list }


def import_gpx(data):
    DEFAULT_DATA_DIR = 'data'
    command = "igotu2gpx --action dump --format gpx"
    args = command.split()
    p = subprocess.Popen(args, stdout=subprocess.PIPE)
    stdout, stderr = p.communicate()
    if len(stdout) == 0:
        raise IOError
    # Process gps for car
    car_color  = data['car_color'].lower()
    car_number = str(data['car_number'])
    # Ensure the folder
    car_dir = ensure_structure(DEFAULT_DATA_DIR, 'gps', car_number, car_color)
    gps_path  = join(car_dir, 'track.gpx')

    # Save track.gpx into folder
    f = open(gps_path, 'w')
    f.write(stdout)
    f.close()

    return stdout


if __name__ == "__main__":
    data = {
        'car_color': 'RED',
        'car_number': 1,
        'image_first_time_hour': 10,
        'image_first_time_minute': 36,
    }
    status_code, stdout = import_gpx(data)
    #print stdout
