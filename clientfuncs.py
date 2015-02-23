from __future__ import absolute_import, division, print_function
import shutil
from PyQt4 import QtCore, QtGui
from os import makedirs, mkdir
from datetime import datetime
import time
import xml.etree.ElementTree as ET
from os.path import isfile, join, exists, splitext, basename
from detecttools.directory import Directory
import traceback
import subprocess
import numpy as np


class CopyThread(QtCore.QThread):
    def __init__(self, filenames, destinations):
        QtCore.QThread.__init__(self)
        self.filenames = filenames
        self.destinations = destinations

    def __del__(self):
        self.wait()

    def run(self):
        for index, f in enumerate(self.filenames):
            filepath = f
            if not isfile(filepath):
                continue
            for outdir in self.destinations:
                if not exists(outdir):
                    makedirs(outdir)
                # time.sleep(2)
                shutil.copy2(filepath, outdir)
                self.emit(QtCore.SIGNAL('file_done'), index, join(outdir, f))
        self.emit(QtCore.SIGNAL('completed'))
        return None


class ImportThread(QtCore.QThread):
    def __init__(thrd, gpswgt):
        QtCore.QThread.__init__(thrd)
        thrd.gpswgt = gpswgt

    def run(thrd):
        #When hooked up to a i-gotu gps dongle
        data = thrd.gpswgt.compile_data()
        thrd.gpswgt.parent.status_bar.showMessage(QtCore.QString("Importing GPS information"))
        try:
            gpx_string = import_gpx(data)
        except IOError:
            thrd.gpswgt.parent.status_bar.showMessage(QtCore.QString("Couldn't import GPS info. Make sure the dongle is connected"))
            thrd.gpswgt.parent.status_bar.setPalette(thrd.gpswgt.error_palette)
            return
        import cv2
        #gpx_string = open("test_gps/track.gpx", "r").read()
        ## Process gps for car
        #car_color  = data['car_color'].lower()
        #car_number = str(data['car_number'])
        ## Ensure the folder
        #car_dir = igotu.ensure_structure('data', 'gps', car_number, car_color)
        #gps_path  = join(car_dir, 'track.gpx')
        #f = open(gps_path, 'w')
        #f.write(gpx_string)
        #f.close()
        gps_json = convert_gpx_to_json(gpx_string)
        if len(gps_json['track']) == 0:
            thrd.gpswgt.parent.status_bar.showMessage(QtCore.QString("No Points found. Import again."))
            thrd.gpswgt.parent.status_bar.setPalette(thrd.gpswgt.error_palette)
            return
        pts = []
        img = cv2.imread(thrd.gpswgt.map_image_file)
        #coord_map = CoordinateMap((-1.32504, 36.766777), (-1.442833, 36.965561), img)     # Nairobi (assets/map_nairobi.png)
        #coord_map = CoordinateMap((42.789920, -73.759957), (42.673663, -73.592416), img)  # Albany  (assets/map_albany.png)
        #coord_map = CoordinateMap((42.740739, -73.697043), (42.720154, -73.657561), img)  # Troy    (assets/map_troy.png)
        coord_map = CoordinateMap((42.735759, -73.686637), (42.726444, -73.664621), img)   # RPI     (assets/map_rpi.png)
        for point in gps_json['track']:
            lat = point['lat']
            lon = point['lon']
            x, y = coord_map.map_point_float((lat, lon))
            pts.append(np.array([x, y]))

        cv2.polylines(img, [np.array(pts, dtype=np.int32)], False, (255, 0, 0), thickness=2)
        cv2.imwrite("figure.png", img)

    def begin(thrd):
        thrd.start()


class CoordinateMap:
    '''
    Maps coordinates to pixels in an image. Does not account for
    curvature of Earth.
    '''
    def __init__(self, ulcoord, brcoord, img):
        img_shape = img.shape
        self.width = img_shape[1]
        self.height = img_shape[0]
        self.ulcoord = ulcoord
        self.brcoord = brcoord
        self.dx, self.dy = self.get_pixel_difference()

    def get_pixel_difference(self):
        # Gets degree / pixel
        import math
        difference_x = math.fabs(self.brcoord[1] - self.ulcoord[1])
        difference_y = math.fabs(self.brcoord[0] - self.ulcoord[0])
        dx = (1.0 * self.width) / difference_x
        dy = (1.0 * self.height) / difference_y
        return dx, dy

    def map_point(self, coord):
        import math
        given_y, given_x = coord
        base_y, base_x = self.ulcoord
        difference_x = math.fabs(given_x - base_x)
        difference_y = math.fabs(given_y - base_y)
        x_loc = int(round((difference_x * self.dx)))
        y_loc = int(round((difference_y * self.dy)))
        if x_loc < 0 or x_loc >= self.width:
            print('Error: point outside image')
            #return (-1, -1)
        if y_loc < 0 or y_loc >= self.height:
            print('Error: point outside image')
            #return (-1, -1)
        return (x_loc, y_loc)

    def map_point_float(self, coord):
        import math
        given_y, given_x = coord
        base_y, base_x = self.ulcoord
        difference_x = math.fabs(given_x - base_x)
        difference_y = math.fabs(given_y - base_y)
        x_loc = (difference_x * self.dx)
        y_loc = (difference_y * self.dy)
        if x_loc < 0 or x_loc >= self.width:
            print('Error: point outside image')
            #return (-1, -1)
        if y_loc < 0 or y_loc >= self.height:
            print('Error: point outside image')
            #return (-1, -1)
        return (x_loc, y_loc)


def find_candidates(search_path, search_str, verbose=False):
    transform_one_list = [
        (lambda x: x),                       # Search for original
        (lambda x: x.lower()),               # Search for lowercase version
        (lambda x: x.upper()),               # Search for uppercase version
    ]
    transform_two_list = [
        (lambda y: y),                       # Search for original
        (lambda y: splitext(y)[0]),          # Search without extension
    ]
    transform_three_list = [
        (lambda z: z),                       # Search for original
        (lambda z: z.replace('.', '')),      # Remove periods
        (lambda z: z.replace('_', '')),      # Remove underscore
        (lambda z: z.replace('-', '')),      # Remove hyphen
        (lambda z: z.replace(' ', '')),      # Remove hyphen
        (lambda z: z.replace('_', '-')),     # Flipped underscore with hyphen
        (lambda z: z.replace('-', '_')),     # Flipped hyphen with underscore
    ]
    transform_list = []
    for transform_three in transform_three_list:
        for transform_two in transform_two_list:
            for transform_one in transform_one_list:
                transform_list.append([transform_three, transform_two, transform_one])

    def transform(string):
        temp = set()
        for transform in transform_list:
            a, b, c = transform
            temp.add( a( b( c( string ) ) ) )
        return sorted(temp)

    direct = Directory(search_path, recursive=True, include_file_extensions='images')
    if verbose:
        print('TESTING FOR %d TRANSFORMS ON %d FILES' % (len(transform_list) ** 2, len(direct.files())))
    found_list = []
    found = False
    for candidate_path in direct.files():
        candidate_str = basename(candidate_path)
        if verbose:
            print('Testing %r' % (candidate_path, ))
        if found:
            if verbose:
                print('    Appending %r' % (candidate_path, ))
            found_list.append(candidate_path)
        else:
            for candidate_ in transform(candidate_str):
                for search_ in transform(search_str):
                    if candidate_ == search_:
                        if verbose:
                            print('    Trying %r == %r - FOUND!' % (candidate_, search_, ))
                        found = True
                        found_list.append(candidate_path)
                    else:
                        if verbose:
                            print('    Trying %r == %r' % (candidate_, search_, ))
                    if found:
                        break
                if found:
                    break
    return found_list


def ex_deco(action_func):
    #import types
    # import inspect
    #import utool as ut
    # #ut.embed()
    # argspec = inspect.getargspec(action_func)

    def logerr(ex, self=None):
        print ('EXCEPTION RAISED! ' + traceback.format_exc(ex))
        log = open('error_log.txt', 'w')
        log.write(traceback.format_exc(ex))
        log.close()
        msg_box = QtGui.QErrorMessage(self)
        msg_box.showMessage(ex.message)
    #is_method = isinstance(action_func, types.MethodType)
    # is_method =  (len(argspec.args) > 0 and argspec.args[0] == 'self')
    def func_wrapper(self, *args):
        # print('+----------<2>')
        # print(action_func)
        # print(argspec)
        # print('self=%r' % (self,))
        # print('args=%r' % (args,))
        # print('L__________')
        try:
            return action_func(self, *args)
        except Exception as ex:
            logerr(ex, self)

    return func_wrapper


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
