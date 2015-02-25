# -*- mode: python -*-
import os
import sys
from os.path import join, exists, abspath

# Pyinstaller Variables (enumerated for readability, not needed)
#Analysis = Analysis  # NOQA

def add_data(a, dst, src):
    def platform_path(path):
        def truepath_relative(path, otherpath=None):
            from os.path import normpath, relpath
            def truepath(path):
                from os.path import normpath, realpath, expanduser
                return normpath(realpath(expanduser(path)))
            if otherpath is None:
                otherpath = truepath(os.getcwd())
            return normpath(relpath(path, otherpath))
        if path == '':
            raise ValueError('path cannot be the empty string')
        # get path relative to cwd
        path1 = truepath_relative(path)
        if sys.platform.startswith('win32'):
            import utool as ut
            path2 = ut.fixwin32_shortname(path1)
        else:
            path2 = path1
        return path2

    global LIB_EXT
    from os.path import dirname, exists
    if dst == '':
        raise ValueError('dst path cannot be the empty string')
    if src == '':
        raise ValueError('src path cannot be the empty string')
    src_ = platform_path(src)
    if not os.path.exists(dirname(dst)) and dirname(dst) != "":
        os.makedirs(dirname(dst))
    _pretty_path = lambda str_: str_.replace('\\', '/')
    # Default datatype is DATA
    dtype = 'DATA'
    # Infer datatype from extension
    #extension = splitext(dst)[1].lower()
    #if extension == LIB_EXT.lower():
    if LIB_EXT[1:] in dst.split('.'):
        dtype = 'BINARY'
    assert exists(src_), 'src_=%r does not exist'
    a.datas.append((dst, src_, dtype))

# Build data before running analysis for quick debugging
DATATUP_LIST = []
BINARYTUP_LIST = []

##################################
# System Variables
##################################
PLATFORM = sys.platform
APPLE = PLATFORM.startswith('darwin')
WIN32 = PLATFORM.startswith('win32')
LINUX = PLATFORM.startswith('linux2')

LIB_EXT = {'win32': '.dll',
           'darwin': '.dylib',
           'linux2': '.so'}[PLATFORM]

##################################
# Asserts
##################################
ibsbuild = ''
root_dir = os.getcwd()
try:
    assert exists(join(root_dir, 'installers.py'))
    assert exists('../gzc-client')
    assert exists(root_dir)
except AssertionError:
    raise Exception('installers.py must be run from gzc-client root')

##################################
# Explicitly add modules in case they are not in the Python PATH
##################################
module_repos = ['utool', 'detecttools']
pathex = ['.', './widgets'] + [ join('..', repo) for repo in module_repos ]
if APPLE:
    # We need to explicitly add the MacPorts and system Python site-packages folders on Mac
    pathex.append('/opt/local/Library/Frameworks/Python.framework/Versions/2.7/lib/python2.7/site-packages/')
    pathex.append('/System/Library/Frameworks/Python.framework/Versions/2.7/lib/python2.7/')

##################################
# QT Gui and HDF5 dependencies
##################################
if APPLE:
    walk_path = '/opt/local/Library/Frameworks/QtGui.framework/Versions/4/Resources/qt_menu.nib'
    for root, dirs, files in os.walk(walk_path):
        for lib_fname in files:
            toc_src = join(walk_path, lib_fname)
            toc_dst = join('qt_menu.nib', lib_fname)
            DATATUP_LIST.append((toc_dst, toc_src))

##################################
# Assets, Libs, and Icon
##################################
walk_path = 'assets'
for root, dirs, files in os.walk(walk_path):
    for icon_fname in files:
        toc_src = join(abspath(root), icon_fname)
        toc_dst = join(root, icon_fname)
        DATATUP_LIST.append((toc_dst, toc_src))

walk_path = 'libs'
for root, dirs, files in os.walk(walk_path):
    for lib_fname in files:
        toc_src = join(abspath(root), lib_fname)
        toc_dst = join(root, lib_fname)
        DATATUP_LIST.append((toc_dst, toc_src))

# App Icon File
ICON_EXT = {'darwin': '.icns',
            'win32':  '.ico',
            'linux2': '.ico'}[PLATFORM]
iconfile = join('_installers', 'ibsicon' + ICON_EXT)
icon_src = join(root_dir, iconfile)
icon_dst = join(ibsbuild, iconfile)
DATATUP_LIST.append((icon_dst, icon_src))

##################################
# Build executable
##################################
# Executable name
exe_name = {'win32':  'build/GZCClientApp.exe',
            'darwin': 'build/pyi.darwin/GZCClientApp/GZCClientApp',
            'linux2': 'build/GZCClientApp.ln'}[PLATFORM]

print('[installer] Checking Data')
for (dst, src) in DATATUP_LIST:
    assert exists(src), 'checkpath for src=%r failed' % (src,)

print('[installer] Running Analysis')
a = Analysis(  # NOQA
    ['client.py'],
    pathex=pathex,
    hiddenimports=[],
    hookspath=None,
    runtime_hooks=None
)

print('[installer] Adding %d Datatups' % (len(DATATUP_LIST,)))
for (dst, src) in DATATUP_LIST:
    add_data(a, dst, src)

print('[installer] Adding %d Binaries' % (len(BINARYTUP_LIST),))
for binarytup in BINARYTUP_LIST:
    a.binaries.append(binarytup)

print('[installer] PYZ Step')
pyz = PYZ(a.pure)   # NOQA

exe_kwargs = {
    'console': True,
    'debug': False,
    'name': exe_name,
    'exclude_binaries': True,
    'append_pkg': False,
}

collect_kwargs = {
    'strip': None,
    'upx': True,
    'name': join('dist', 'gzc-client')
}

# Windows only EXE options
if WIN32:
    exe_kwargs['icon'] = join(root_dir, iconfile)
    #exe_kwargs['version'] = 1.5
if APPLE:
    exe_kwargs['console'] = False

# Pyinstaller will gather .pyos
print('[installer] EXE Step')
opt_flags = [('O', '', 'OPTION')]
exe = EXE(pyz, a.scripts + opt_flags, **exe_kwargs)   # NOQA

print('[installer] COLLECT Step')
coll = COLLECT(exe, a.binaries, a.zipfiles, a.datas, **collect_kwargs)  # NOQA

bundle_name = 'GZCClient'
if APPLE:
    bundle_name += '.app'

print('[installer] BUNDLE Step')
app = BUNDLE(coll, name=join('dist', bundle_name))  # NOQA
