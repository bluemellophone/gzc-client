#!/usr/bin/env python
from __future__ import absolute_import, division, print_function
from os.path import dirname, realpath, join, exists, normpath
import utool as ut
import sys
from os.path import join  # NOQA


def get_setup_dpath():
    assert exists('../gzc-client'), 'must be run in gzc-client directory'
    cwd = normpath(realpath(dirname(__file__)))
    return cwd


def clean_pyinstaller():
    print('[installer] +--- CLEAN_PYINSTALLER ---')
    cwd = get_setup_dpath()
    ut.remove_files_in_dir(cwd, 'GZCClient.pkg', recursive=False)
    ut.remove_files_in_dir(cwd, 'GZCClientApp.pkg', recursive=False)
    ut.remove_files_in_dir(cwd, 'qt_menu.nib', recursive=False)
    ut.remove_files_in_dir(cwd, 'qt_menu.nib', recursive=True)
    ut.delete(join(cwd, 'dist/gzc-client'))
    ut.delete(join(cwd, 'gzc-client-win32-setup.exe'))
    ut.delete(join(cwd, 'build'))
    ut.delete(join(cwd, 'dist'))
    print('[installer] L___ FINSHED CLEAN_PYINSTALLER ___')


def build_pyinstaller():
    """
    build_pyinstaller creates build/gzc-client/* and dist/gzc-client/*
    """
    print('[installer] +--- BUILD_PYINSTALLER ---')
    # 1) RUN: PYINSTALLER
    # Run the pyinstaller command (does all the work)
    if ut.WIN32:
        #ut.cmd('pyinstaller', '--runtime-hook', 'rthook_pyqt4.py', '_installers/pyinstaller-client.spec', '-y')
        ut.cmd('pyinstaller --runtime-hook rthook_pyqt4.py _installers/pyinstaller-client.spec -y')
    else:
        ut.cmd('pyinstaller', '_installers/pyinstaller-client.spec', '-y')
    #ut.cmd('pyinstaller', '--runtime-hook rthook_pyqt4.py', '_installers/pyinstaller-client.spec')
    # 2) POST: PROCESSING
    # Perform some post processing steps on the mac

    # if sys.platform == 'darwin' and exists('dist/GZCClient.app/Contents/'):
    #     copy_list = [
    #         ('ibsicon.icns', 'Resources/icon-windowed.icns'),
    #         ('Info.plist', 'Info.plist'),
    #     ]
    #     srcdir = '_installers'
    #     dstdir = 'dist/GZCClient.app/Contents/'
    #     for srcname, dstname in copy_list:
    #         src = join(srcdir, srcname)
    #         dst = join(dstdir, dstname)
    #         ut.copy(src, dst)
    print('[installer] L___ FINISH BUILD_PYINSTALLER ___')
    # ut.cmd('./_scripts/mac_dmg_builder.sh')


def ensure_inno_isinstalled():
    """ Ensures that the current machine has INNO installed. returns path to the
    executable """
    assert ut.WIN32, 'Can only build INNO on windows'
    inno_fpath = ut.search_in_dirs('Inno Setup 5\ISCC.exe', ut.get_install_dirs())
    # Make sure INNO is installed
    if inno_fpath is None:
        print('WARNING: cannot find inno_fpath')
        AUTO_FIXIT = ut.WIN32
        print('Inno seems to not be installed. AUTO_FIXIT=%r' % AUTO_FIXIT)
        if AUTO_FIXIT:
            print('Automaticaly trying to downoad and install INNO')
            # Download INNO Installer
            inno_installer_url = 'http://www.jrsoftware.org/download.php/ispack.exe'
            inno_installer_fpath = ut.download_url(inno_installer_url)
            print('Automaticaly trying to install INNO')
            # Install INNO Installer
            ut.cmd(inno_installer_fpath)
        else:
            inno_homepage_url = 'http://www.jrsoftware.org/isdl.php'
            ut.open_url_in_browser(inno_homepage_url)
            raise AssertionError('Cannot find INNO and AUTOFIX it is false')
        # Ensure that it has now been installed
        inno_fpath = ut.search_in_dirs('Inno Setup 5\ISCC.exe', ut.get_install_dirs())
        assert ut.checkpath(inno_fpath, verbose=True, info=True), 'inno installer is still not installed!'
    return inno_fpath


def ensure_inno_script():
    """ writes inno script to distk """
    cwd = get_setup_dpath()
    iss_script_fpath = join(cwd, '_installers', 'win_installer_script.iss')
    # THE ISS USES {} AS SYNTAX. CAREFUL
    #app_publisher = 'Rensselaer Polytechnic Institute'
    #app_name = 'GZCClient'
    iss_script_code = ut.codeblock(
        '''
        ; Script generated by the Inno Setup Script Wizard.
        ; SEE THE DOCUMENTATION FOR DETAILS ON CREATING INNO SETUP SCRIPT FILES!
        ; http://www.jrsoftware.org/isdl.php

        [Setup]
        ; NOTE: The value of AppId uniquely identifies this application.
        ; Do not use the same AppId value in installers for other applications.
        ; (To generate a new GUID, click Tools | Generate GUID inside the IDE.)
        AppId={{47BE3DA2-261D-4672-9849-18BB2EB382FC}
        AppName=GZCClient
        AppVersion=1
        ;AppVerName=GZCClient 1
        AppPublisher=Rensselaer Polytechnic Institute
        AppPublisherURL=www.rpi.edu/~crallj/
        AppSupportURL=www.rpi.edu/~crallj/
        AppUpdatesURL=www.rpi.edu/~crallj/
        DefaultDirName={pf}\GZCClient
        DefaultGroupName=GZCClient
        OutputBaseFilename=gzc-client-win32-setup
        SetupIconFile=ibsicon.ico
        Compression=lzma
        SolidCompression=yes

        [Languages]
        Name: "english"; MessagesFile: "compiler:Default.isl"

        [Tasks]
        Name: "desktopicon"; Description: "{cm:CreateDesktopIcon}"; GroupDescription: "{cm:AdditionalIcons}"; Flags: unchecked

        [Files]
        Source: "..\dist\gzc-client\GZCClientApp.exe"; DestDir: "{app}"; Flags: ignoreversion
        Source: "..\dist\gzc-client\*"; DestDir: "{app}"; Flags: ignoreversion recursesubdirs createallsubdirs
        ; NOTE: Don't use "Flags: ignoreversion" on any shared system files

        [Icons]
        Name: "{group}\gzc-client"; Filename: "{app}\GZCClientApp.exe"
        Name: "{commondesktop}\gzc-client"; Filename: "{app}\GZCClientApp.exe"; Tasks: desktopicon

        [Run]
        Filename: "{app}\GZCClientApp.exe"; Description: "{cm:LaunchProgram,GZCClient}"; Flags: nowait postinstall skipifsilent
        '''
    )
    ut.write_to(iss_script_fpath, iss_script_code, onlyifdiff=True)
    assert ut.checkpath(iss_script_fpath, verbose=True, info=True), 'cannot find iss_script_fpath'
    return iss_script_fpath


def inno_installer_postprocess():
    """ Move the built installer into a more reasonable directory """
    try:
        cwd = get_setup_dpath()
        installer_src = join(cwd, '_installers', 'Output', 'gzc-client-win32-setup.exe')
        installer_dst = join(cwd, 'dist', 'gzc-client-win32-setup.exe')
        # Make a timestamped version
        timestamped_fname = 'gzc-client-win32-setup-{timestamp}.exe'.format(timestamp=ut.get_timestamp())
        installer_dst2 = join(cwd, 'dist', timestamped_fname)
        ut.move(installer_src, installer_dst)
        ut.copy(installer_dst, installer_dst2)
    except Exception as ex:
        ut.printex(ex, 'error moving setups', iswarning=True)


def build_win32_inno_installer():
    """ win32 self-executable package """
    print('[installer] +--- BUILD_WIN32_INNO_INSTALLER ---')
    assert ut.WIN32, 'Can only build INNO on windows'
    # Get inno executable
    inno_fpath = ensure_inno_isinstalled()
    # Get GZCClient inno script
    iss_script_fpath = ensure_inno_script()
    print('Trying to run ' + ' '.join(['"' + inno_fpath + '"', '"' + iss_script_fpath + '"']))
    try:
        command_args = ' '.join((inno_fpath, iss_script_fpath))
        ut.cmd(command_args)
    except Exception as ex:
        ut.printex(ex, 'error running script')
        raise
    # Move the installer into dist and make a timestamped version
    inno_installer_postprocess()
    # Uninstall exe in case we need to cleanup
    #uninstall_gzc-client_exe = 'unins000.exe'
    print('[installer] L___ BUILD_WIN32_INNO_INSTALLER ___')


def package_installer():
    """
    system dependent post pyinstaller step
    """
    print('[installer] +--- PACKAGE_INSTALLER ---')
    #build_win32_inno_installer()
    if sys.platform.startswith('win32'):
        build_win32_inno_installer()
    elif sys.platform.startswith('darwin'):
        # ut.cmd('sudo ./_installers/mac_dmg_builder.sh')
        pass
    elif sys.platform.startswith('linux'):
        raise NotImplementedError('no linux packager (rpm or deb) supported. try running with --build')
        pass
    print('[installer] L___ FINISH PACKAGE_INSTALLER ___')


def test_app():
    print('[installer] +--- TEST_APP ---')
    ut.cmd(ut.unixpath('dist/gzc-client/GZCClientApp.exe'))
    print('[installer] L___ FINISH TEST_APP ___')
    #ut.cmd(ut.unixpath('dist/gzc-client/gzc-client-win32-setup.exe'))


def main():
    """
    CommandLine:
        python installers.py --all
        python installers.py --inno

    """
    print('For a full run use: python installers.py --all')
    print('[installer] +--- MAIN ---')
    BUILD_APP       = ut.get_argflag(('--build'))
    BUILD_INSTALLER = ut.get_argflag(('--inno', '--package', '--pkg'))
    TEST_APP        = ut.get_argflag(('--test'))
    CLEAN_BUILD     = ut.get_argflag(('--clean'))
    ALL             = ut.get_argflag('--all')

    # default behavior is full build
    BUILD_ALL = ALL or not (BUILD_APP or BUILD_INSTALLER or TEST_APP)

    # 1) SETUP: CLEAN UP
    if CLEAN_BUILD or BUILD_ALL:
        clean_pyinstaller()
    if BUILD_APP or BUILD_ALL:
        build_pyinstaller()
    if BUILD_INSTALLER or BUILD_ALL:
        package_installer()
    # if TEST_APP or BUILD_ALL:
    #     test_app()
    print('[installer] L___ FINISH MAIN ___')


if __name__ == '__main__':
    main()

'''
dist\gzc-client-win32-setup.exe
dist\gzc-client\GZCClientApp.exe
'''
