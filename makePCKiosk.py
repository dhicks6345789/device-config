#!/usr/bin/python3

# Standard libraries.
import os

print("Configuring...")

configHandle = open("/etc/xdg/lxsession/LXDE-pi/autostart","w")
# To do: check these settings work okay.
configHandle.write("xset s noblank\n")
configHandle.write("xset s off\n")
configHandle.write("xset -dpms\n")
configHandle.write("point-rpi\n")
configHandle.write("/usr/bin/chromium --incognito --start-maximized --no-default-browser-check --kiosk https://remote.knightsbridgeschool.com\n")
configHandle.close()

configString = ""
configHandle = open("/boot/grub/grub.cfg")
for configLine in configHandle.readlines():
  configLine.replace("timeout=5","timeout=0")
  configString = configString + configLine
configHandle.close()

configHandle = open("/boot/grub/grub.conf","w")
configHandle.write(configString)
configHandle.close()

os.system("reboot")
