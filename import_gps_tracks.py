import subprocess
import requests
import simplejson as json
from os.path import join, exists  # NOQA
from os import mkdir


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


def import_gpx(domain, data):
    GPSURL = domain + '/gps/submit'
    DEFAULT_DATA_DIR = 'data'
    command = "igotu2gpx --action dump --format gpx"
    args = command.split()
    p = subprocess.Popen(args, stdout=subprocess.PIPE)
    stdout, stderr = p.communicate()

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

    # gps data
    content = open(join('test_gps', 'track.gpx'), 'rb')
    files = {
        'gps_data': content,
    }
    print content

    r = requests.post(GPSURL, data=data, files=files)
    print("HTTP STATUS:", r.status_code)
    response = json.loads(r.text)
    print("RESPONSE:", response)
    return stdout


if __name__ == "__main__":
    data = {
        'car_color': 'RED',
        'car_number': 3,
        'image_first_time_hour': 10,
        'image_first_time_minute': 36,
    }
    stdout = import_gpx("http://localhost:5000", data)
    #print stdout
