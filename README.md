# Device Config
A library of scripts to set up a specific development / runtime environment on an Operating System - the target might be a VM or a physical device. Made with the setup of dedicated thin client / kiosk devices in mind, in particular using the Raspberry Pi and the associated (Debian-based) Raspberry Pi OS both on the Pi itself and on Intel machines.

**Important Note: Some of these scripts are designed to configure the way a physical or virtual machine boots and loads applications and the user interface. They are for use on devices (Raspberry Pis, old PCs) you are aiming to use as dedicated kiosk / thin client machines, not for running on a typical desktop PC.**

## Installation & Usage
The most convienient way to to run an individual script is by using curl to download and run it in one line - example command lines are given for each script.

You can also download the repository from Github. The scripts are written in Python, you will need to have Python installed (generally a default on most Linux distributions). Some scripts use other libraries / utilities, such as Expect, the scripts themselves will take care of installation if needed.

### configKiosk
Configures a machine to be a "kiosk", loading nothing but a web browser pointing at a specified URL. Works on Raspberry Pi OS (both on the Pi and Intel versions). Can be useful, for instance, for digital signage applications - plug a Raspberry Pi into a large screen display, configure with this script, reboot and away you go.

The following example displays a simple Google Slides document on a loop, with 5 seconds between each page of the slideshow.

```
curl -s https://www.sansay.co.uk/device-config/configKiosk.py > config.py; sudo python3 config.py --URL https://docs.google.com/presentation/d/e/2PACX-1vRyBGWp7WzWYwkhgSPoVSmaihvJm7rfCpg7AKginEDP0dHrbGIYk9S0sAIF7m8O3V8GT3x0-o2es4Re/pub?start=true\\\&loop=true\\\&delayms=5000; rm config.py
```

Note that, in the above example, the ampersands in the given URL need to be double-escaped, i.e. "\\\\\&".

### configExamMachine
Configures a machine to be a kiosk device running [ExamWritePad](https://sheldnet.co.uk/examwritepad/) - no desktop, no user access to a web browser, but does have network access and can save work both locally and to network storage.

Start with a freshly-installed [Raspberry Pi OS](https://www.raspberrypi.com/software/) machine, either an actual Raspberry Pi or a x86 laptop / desktop. Then, run the command below:

```
curl -s https://www.sansay.co.uk/device-config/configExamMachine.py | sudo bash
```
