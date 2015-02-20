from __future__ import absolute_import, division, print_function
import shutil
import PyQt4
from PyQt4 import QtCore, QtGui
from os import makedirs
from os.path import isfile, join, exists, splitext, basename
from detecttools.directory import Directory


class CopyThread(QtCore.QThread):
    def __init__(self, filenames, destinations):
        QtCore.QThread.__init__(self)
        self.filenames = filenames
        self.destinations = destinations

    def __del__(self):
        self.wait()

    def run(self):
        for f in self.filenames:
            filepath = f
            if not isfile(filepath):
                continue
            for outdir in self.destinations:
                if not exists(outdir):
                    makedirs(outdir)
                # time.sleep(2)
                shutil.copy2(filepath, outdir)
                self.emit(QtCore.SIGNAL('file_done'), (join(outdir, f)))
        self.emit(QtCore.SIGNAL('completed'))
        return None


class CoordinateMap:
    """
    Maps coordinates to pixels in an image. Does not account for
    curvature of Earth.
    """
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
            print("Error: point outside image")
            #return (-1, -1)
        if y_loc < 0 or y_loc >= self.height:
            print("Error: point outside image")
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
            print("Error: point outside image")
            #return (-1, -1)
        if y_loc < 0 or y_loc >= self.height:
            print("Error: point outside image")
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
        print("TESTING FOR %d TRANSFORMS ON %d FILES" % (len(transform_list) ** 2, len(direct.files())))
    found_list = []
    found = False
    for candidate_path in direct.files():
        candidate_str = basename(candidate_path)
        if verbose:
            print("Testing %r" % (candidate_path, ))
        if found:
            if verbose:
                print("    Appending %r" % (candidate_path, ))
            found_list.append(candidate_path)
        else:
            for candidate_ in transform(candidate_str):
                for search_ in transform(search_str):
                    if candidate_ == search_:
                        if verbose:
                            print("    Trying %r == %r - FOUND!" % (candidate_, search_, ))
                        found = True
                        found_list.append(candidate_path)
                    else:
                        if verbose:
                            print("    Trying %r == %r" % (candidate_, search_, ))
                    if found:
                        break
                if found:
                    break
    return found_list
