# Device Config
A library of scripts to set up a specific development / runtime environment on an Operating System - the target might be a VM or a physical device. Made with the setup of dedicated thin client / kiosk devices in mind, in particular using the Raspberry Pi and the associated (Debian-based) Raspberry Pi OS both on the Pi itself and on Intel machines.

**Important Note: Some of these scripts are designed to configure the way a physical or virtual machine boots and loads applications and the user interface. They are for use on devices (Raspberry Pis, old PCs) you are aiming to use as dedicated kiosk / thin client machines, not for running on a typical desktop PC.**

## Installation & Usage
You can download the repository from Github. The scripts are written in Python, you will need to have Python installed (generally a default on most Linux distributions). Some scripts use other libraries / utilities, such as Expect, the scripts themselves will take care of installation if needed.

Each named script in the repository includes a common library file, deviceConfig.py. A "compiled" version is available that combines this library file into one file, ready to download and run with a single command.

### configKiosk
Configures a machine to be a "kiosk", loading nothing but a web browser pointing at a specified URL. Works on Raspberry Pi OS (both on the Pi and Intel versions). Can be useful, for instance, for digital signage applications - plug a Raspberry Pi into a large screen display, configure with this script, reboot and away you go.

The following example displays a simple Google Slides document on a loop, with 5 seconds between each page of the slideshow.

```
curl -s https://www.sansay.co.uk/device-config/configKiosk.py > config.py; sudo python3 config.py --URL https://docs.google.com/presentation/d/e/2PACX-1vRyBGWp7WzWYwkhgSPoVSmaihvJm7rfCpg7AKginEDP0dHrbGIYk9S0sAIF7m8O3V8GT3x0-o2es4Re/pub?start=true\\\&loop=true\\\&delayms=5000; rm config.py
```

Note that, in the above example, the ampersands in the given URL need to be double-escaped, i.e. "\\\\\&".

### configWebBrowsingMachine
Configures a machine to be a basic web-browsing machine, loading up a full-screen incognito-mode web browser on boot and nothing else. Useful as a web-only thin-client device for public workstations. The browser can start up with a list of URLs to load, so you can set your thin client to load a home page or whatever you want.

### configExamClock
Configures a machine to be an "exam clock" - simply boots up and displays the time in as large a font as possible. Handy for exam situations if you happen to have a Raspberry Pi or old PC you want to dedicate to being a clock device.
