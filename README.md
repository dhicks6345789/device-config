# device-config
A library of scripts to set up a specific development / runtime environment on a Operating System - the target might be a VM or a physical device. Made with the setup of dedicated thin client / kiosk devices in mind.

## Installation
You can download the repository from Github. Each named script in the repository includes a common library file, deviceConfig.py. A "compiled" version is available that combines this library file into one file, ready to download and run with no further dependancies. For example:
```
curl -s https://www.sansay.co.uk/device-config/configKiosk.py > config.py; sudo python3 config.py --URL https://www.google.com --restartOrShutdown r; rm config.py
```

## Notes
* Python with Hugo run environment
* GOV.UK / Jekyll run environment
* US Gov run environment?
* If wireless hardware present:
  * Option: initial setup via self-hosted wireless network
  * Separate application: Wireless network picker
* BigClown console / server
* Configure RClone
* Code for data sync application
  * Pick startup application
  * Chromium
  * Option: wireless signal / battery / volume / shortcut homepage as default "new tab" homepage
  * Option: Kiosk
  * Option: URL(s)
  * Default: localhost for homepage
  * Option: Refresh when file (GDrive) updated
  * Configure RClone...
  * LogIT uLog Sensorlab (x86 only)
  * Configure RClone
  * Add VNC (x86, so not built-in RealVNC)
  * Add NoVNC
