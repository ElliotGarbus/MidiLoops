; Script generated by the Inno Setup Script Wizard.
; SEE THE DOCUMENTATION FOR DETAILS ON CREATING INNO SETUP SCRIPT FILES!

#define MyAppName "BackingTrackPlayer"
#define MyAppVersion "1.11"
#define MyAppPublisher "Elliot Garbus"
#define MyAppURL "https://github.com/ElliotGarbus/BackingTrackPlayer/releases"
#define MyAppExeName "Backing Track Player.exe"

[Setup]
; NOTE: The value of AppId uniquely identifies this application. Do not use the same AppId value in installers for other applications.
; (To generate a new GUID, click Tools | Generate GUID inside the IDE.)
AppId={{82A90AAC-6145-4E72-8767-0C79F044E02E}
AppName={#MyAppName}
AppVersion={#MyAppVersion}
;AppVerName={#MyAppName} {#MyAppVersion}
AppPublisher={#MyAppPublisher}
AppPublisherURL={#MyAppURL}
AppSupportURL={#MyAppURL}
AppUpdatesURL={#MyAppURL}
DefaultDirName={autopf}\{#MyAppName}
DisableProgramGroupPage=yes
LicenseFile=C:\Users\ellio\PycharmProjects\BackingTrackPlayer\LICENSE
; Uncomment the following line to run in non administrative install mode (install for current user only.)
;PrivilegesRequired=lowest
OutputDir=C:\Users\ellio\PycharmProjects\BackingTrackPlayer\BackingTrackPlayerDist\output
OutputBaseFilename=BackingTrackPlayerWindowsInstaller
SetupIconFile=C:\Users\ellio\PycharmProjects\BackingTrackPlayer\icons8_refresh_64_icon.ico
Compression=lzma
SolidCompression=yes
WizardStyle=modern

[Languages]
Name: "english"; MessagesFile: "compiler:Default.isl"

[Tasks]
Name: "desktopicon"; Description: "{cm:CreateDesktopIcon}"; GroupDescription: "{cm:AdditionalIcons}"; Flags: unchecked

[Files]
Source: "C:\Users\ellio\PycharmProjects\BackingTrackPlayer\BackingTrackPlayerDist\dist\Backing Track Player\Backing Track Player.exe"; DestDir: "{app}"; Flags: ignoreversion
Source: "C:\Users\ellio\PycharmProjects\BackingTrackPlayer\BackingTrackPlayerDist\dist\Backing Track Player\*"; DestDir: "{app}"; Flags: ignoreversion recursesubdirs createallsubdirs
; NOTE: Don't use "Flags: ignoreversion" on any shared system files

[Icons]
Name: "{autoprograms}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"
Name: "{autodesktop}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"; Tasks: desktopicon

[Run]
Filename: "{app}\{#MyAppExeName}"; Description: "{cm:LaunchProgram,{#StringChange(MyAppName, '&', '&&')}}"; Flags: nowait postinstall skipifsilent

