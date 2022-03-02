# device-config
A library of scripts to set up a specific development / runtime environment on an Operating System - the target might be a VM or a physical device. Made with the setup of dedicated thin client / kiosk devices in mind, in particular using the Raspberry Pi and the associated (Debian-based) Raspberry Pi OS both on the Pi itself and on Intel machines.

## Installation & Usage
You can download the repository from Github. The scripts are written in Python, you will need to have Python installed (generally a default on most Linux distributions). Some scripts use other libraries / utilities, such as Expect, the scripts themselves will take care of installation if needed.

Each named script in the repository includes a common library file, deviceConfig.py. A "compiled" version is available that combines this library file into one file, ready to download and run with a single command.

### configKiosk
Configures a machine to be a "kiosk", loading nothing but a web browser pointing at a specified URL. Works on Raspberry Pi OS (both on the Pi and Intel versions). Can be useful, for instance, for digital signage applications - plug a Raspberry Pi into a large screen display, configure with this script, reboot and away you go.

The following example displays a simple Google Slides document on a loop, with 5 seconds between each page of the slideshow.

```
curl -s https://www.sansay.co.uk/device-config/configKiosk.py > config.py; sudo python3 config.py --URL https://docs.google.com/presentation/d/e/2PACX-1vRyBGWp7WzWYwkhgSPoVSmaihvJm7rfCpg7AKginEDP0dHrbGIYk9S0sAIF7m8O3V8GT3x0-o2es4Re/pub?start=true\&loop=true\&delayms=5000; rm config.py
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
