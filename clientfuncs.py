from __future__ import absolute_import, division, print_function
import shutil
import sys
from PyQt4 import QtCore, QtGui
from os import makedirs, mkdir
from os.path import isfile, join, exists, splitext, basename, dirname
from detecttools.directory import Directory
import traceback
import subprocess


def resource_path(relative_path, _file='.'):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except AttributeError:
        base_path = dirname(_file)
    path = join(base_path, relative_path)
    print('[clientfuncs] returning resource path = %r' % (path,))
    if not exists(path):
        print('... WARNING path does not exist')
    return path


IGOTU2GPX_BASE = resource_path(join('libs', 'igotu2gpx'))


def ex_deco(action_func):
    #import types
    # import inspect
    #import utool as ut
    # #ut.embed()
    # argspec = inspect.getargspec(action_func)

    def logerr(ex, self=None):
        print ('EXCEPTION RAISED! ' + traceback.format_exc(ex))
        # log = open('error_log.txt', 'w')
        # log.write(traceback.format_exc(ex))
        # log.close()
        try:
            msg_box = QtGui.QErrorMessage(self)
        except:
            msg_box = QtGui.QErrorMessage(self.parent())
        msg_box.showMessage(str(ex.message))

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


class CopyFiles(QtCore.QThread):
    def __init__(self, filenames, destinations):
        print('[CopyFiles] __init__')
        QtCore.QThread.__init__(self)
        self.filenames = filenames
        self.destinations = destinations

    def __del__(self):
        # IT IS DANGEROUS TO OVERRIDE __DEL__ CAN THIS BE REMOVED?
        self.wait()

    def run(self):
        length = len(self.filenames)
        for index, filepath in enumerate(self.filenames):
            if not isfile(filepath):
                continue
            for outdir in self.destinations:
                if not exists(outdir):
                    makedirs(outdir)
                shutil.copy2(filepath, outdir)
                self.emit(QtCore.SIGNAL('fileCopied'), index, length, join(outdir, filepath))
        self.emit(QtCore.SIGNAL('completed'), self.filenames)


class ExtractGPS(QtCore.QThread):
    def __init__(self):
        print('[ExtractGPS] __init__')
        QtCore.QThread.__init__(self)

    def __del__(self):
        # IT IS DANGEROUS TO OVERRIDE __DEL__ CAN THIS BE REMOVED?
        self.wait()

    def findLib(self):
        print('[ExtractGPS] FINDING LIB FOR SYSTEM: %r' % (sys.platform, ))
        if sys.platform.startswith('darwin'):
            self.igotu2gpx_path = join(IGOTU2GPX_BASE, 'darwin', 'MacOS', 'igotu2gpx')
        elif sys.platform.startswith('win32') or sys.platform.startswith('cygwin'):
            self.igotu2gpx_path = join(IGOTU2GPX_BASE, 'win32', 'bin', 'igotu2gpx.exe')
        else:
            msg = '\n'.join([
                'Automatic i-GotU extraction is not operational on this machine.',
                ' sys.platform=%r' % (sys.platform,),
                ' Use \'Manually Select GPX File\' from the File menu',
            ])
            raise NotImplementedError(msg)

    def contactDongle(self):
        print('[ExtractGPS] contactDongle')
        args = [self.igotu2gpx_path, '--action', 'info', '2>&1']
        print('[ExtractGPS] running: ' + ' '.join(args))
        p = subprocess.Popen(' '.join(args), stdout=subprocess.PIPE, shell=True)
        try:
            for line in p.stdout:
                # print(line)
                if 'Unable to download' in line:
                    raise RuntimeError('i-GotU Libs working! ...as far as I can tell')
                    # raise RuntimeError('i-GotU GPS dongle not connected.  Check connection and try again.')
        except IOError as ex:
            print('[ExtractGPS] Caught IOError:')
            print('ex = %s' % (str(ex),))
            pass

    def run(self):
        gpx_content = []
        try:
            # Ensure can find libs and connected
            self.findLib()
            self.contactDongle()
            # Run import
            args = [self.igotu2gpx_path, '--action', 'dump', '2>&1']
            print('[FindLib.run] ' + ' '.join(args))
            p = subprocess.Popen(' '.join(args), stdout=subprocess.PIPE, shell=True)
            try:
                for line in p.stdout:
                    # print(line)
                    if 'Downloaded block' in line:
                        line = line.strip().split()
                        index, length = line[-1].split('/')
                        self.emit(QtCore.SIGNAL('trackExtracted'), index, length, '')
                    elif 'Unable to download' in line:
                        raise RuntimeError('i-GotU GPS dongle has been disconnected during import.  Check connection and try again.')
                    elif 'Downloading tracks' not in line:
                        gpx_content.append(line)
                    else:
                        print('IGNORING LINE: %s' % (line.strip(), ))
            except IOError as ex:
                print('[ExtractGPS] Caught IOError:')
                print('ex = %s' % (str(ex),))
        except RuntimeError as rte:
            self.emit(QtCore.SIGNAL('__EXCEPTION__'), rte)
        self.emit(QtCore.SIGNAL('completed'), ''.join(gpx_content))


@ex_deco
def find_candidates(search_path, search_str, verbose=False):
    print('[clientfuncs.find_candidates]')
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
    search_str = search_str.strip()
    if len(search_str) == 0:
        return direct.files()
    if verbose:
        print('[clientfuncs.find_candidates] TESTING FOR %d TRANSFORMS ON %d FILES' % (len(transform_list) ** 2, len(direct.files())))
    found_list = []
    found = False
    for candidate_path in direct.files():
        candidate_str = basename(candidate_path)
        if verbose:
            print('Testing %r' % (candidate_path, ))
        # First check if search_str is digit and candidate_str ends with that digit
        if search_str.isdigit() and splitext(candidate_str)[0].endswith(search_str):
            print('    Trying %r == %r - FOUND! (ENDSWITH)' % (candidate_str, search_str, ))
            found = True
            found_list.append(candidate_path)
        if found:
            if verbose:
                print('    Appending %r' % (candidate_path, ))
            found_list.append(candidate_path)
        else:
            for candidate_ in transform(candidate_str):
                for search_ in transform(search_str):
                    if candidate_ == search_:
                        print('    Trying %r == %r - FOUND! (TRANDFORM)' % (candidate_, search_, ))
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


# @ex_deco
def ensure_structure(data, kind, car_number, car_color, person=None):
    print('[clientfuncs.ensure_structure]')
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
    person = person.lower()
    person_dir = join(car_dir, person)
    if not exists(person_dir):
        mkdir(person_dir)
    # Return peron dir
    return person_dir
