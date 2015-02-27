; Script generated by the Inno Setup Script Wizard.
; SEE THE DOCUMENTATION FOR DETAILS ON CREATING INNO SETUP SCRIPT FILES!
; http://www.jrsoftware.org/isdl.php

[Setup]
; NOTE: The value of AppId uniquely identifies this application.
; Do not use the same AppId value in installers for other applications.
; (To generate a new GUID, click Tools | Generate GUID inside the IDE.)
AppId={{A57C5DDA-4623-4CB0-8964-E95326706904}
AppName=GZCClient
AppVersion=1
;AppVerName=GZCClient 1
AppPublisher=Rensselaer Polytechnic Institute
AppPublisherURL=ibeis.org
AppSupportURL=ibeis.org
AppUpdatesURL=ibeis.org
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
