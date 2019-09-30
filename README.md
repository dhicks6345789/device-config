# device-config
A script to set up a specific development / runtime environment on a Operating System - the target might be a VM or a physical device. Made with the setup of dedicated thin client / kiosk devices in mind.

## Installation
curl -s https://raw.githubusercontent.com/dhicks6345789/device-config/master/config.py > config.py; sudo python3 config.py

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
