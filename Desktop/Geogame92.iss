; Inno Setup script for the Windows installer of the desktop game.
; Build Geogame92.exe first (pyinstaller --noconfirm Geogame92.spec), then:
;   ISCC.exe /DMyAppVersion=1.1 Geogame92.iss
; (done automatically by .github/workflows/build-windows.yml)

#define MyAppName "GeoGame"
#ifndef MyAppVersion
  #define MyAppVersion "1.1"
#endif
#define MyAppPublisher "Yiannis Kontos & Konstantinos Koutridis"
#define MyAppURL "https://github.com/kkoutrid/GeoGame-Dissertation"
#define MyAppExeName "Geogame92.exe"

[Setup]
; Same AppId as the Geogame91 installer (v1.0), so installing this version
; upgrades an existing installation in place instead of adding a second one.
AppId={{9DA1BD06-424E-46D1-814A-1F4A4D47AC35}
AppName={#MyAppName}
AppVersion={#MyAppVersion}
AppPublisher={#MyAppPublisher}
AppPublisherURL={#MyAppURL}
AppSupportURL={#MyAppURL}
DefaultDirName={autopf}\{#MyAppName}
DefaultGroupName={#MyAppName}
AllowNoIcons=yes
; Install for the current user only (no administrator rights needed).
PrivilegesRequired=lowest
OutputDir=installer_build
OutputBaseFilename=Geogame92_Setup
SetupIconFile=Geogame.ico
UninstallDisplayIcon={app}\{#MyAppExeName}
Compression=lzma
SolidCompression=yes
WizardStyle=modern

[Languages]
Name: "english"; MessagesFile: "compiler:Default.isl"

[Tasks]
Name: "desktopicon"; Description: "{cm:CreateDesktopIcon}"; GroupDescription: "{cm:AdditionalIcons}"; Flags: unchecked

[InstallDelete]
; Leftovers of the 1.0 (Geogame91) install when upgrading.
Type: files; Name: "{app}\Geogame91.exe"
Type: files; Name: "{group}\Geogame 91.lnk"
Type: files; Name: "{autodesktop}\Geogame 91.lnk"

[Files]
Source: "dist\{#MyAppExeName}"; DestDir: "{app}"; Flags: ignoreversion

[Icons]
Name: "{group}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"
Name: "{group}\{cm:ProgramOnTheWeb,{#MyAppName}}"; Filename: "{#MyAppURL}"
Name: "{autodesktop}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"; Tasks: desktopicon

[Run]
Filename: "{app}\{#MyAppExeName}"; Description: "{cm:LaunchProgram,{#StringChange(MyAppName, '&', '&&')}}"; Flags: nowait postinstall skipifsilent
