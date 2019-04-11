#!/usr/bin/python3

# Standard libraries.
import os
import sys

print("Configuring... Bananas")

if os.path.exists("/usr/bin/chromium"):
  chromiumPath = "/usr/bin/chromium"
elif os.path.exists("/usr/bin/chromium-browser"):
  chromiumPath = "/usr/bin/chromium-browser"
else:
  print("Error - Chromium not installed.")
  sys.exit(1)

print("Re-writing GUI Autostart file.")
configHandle = open("/etc/xdg/lxsession/LXDE-pi/autostart","w")
configHandle.write("xset s noblank\n")
configHandle.write("xset s off\n")
configHandle.write("xset -dpms\n")
configHandle.write("point-rpi\n")
configHandle.write(chromiumPath + " --incognito --start-maximized --no-default-browser-check --kiosk https://remote.knightsbridgeschool.com\n")
configHandle.close()

if os.path.exists("/boot/grub/grub.cfg"):
  print("Removing boot timeout from grub.conf.")
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