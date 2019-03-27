#!/usr/bin/python3

# Standard libraries.
import os

print("Configuring...")

configHandle = open("/etc/xdg/lxsession/LXDE-pi/autostart","w")
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

#os.makedirs("/home/pi/.config/autostart", exist_ok=True)
#configHandle = open("/home/pi/.config/autostart/kiosk.desktop", "w")
#configHandle.write("[Desktop Entry]\n")
#configHandle.write("Type=application\n")
#configHandle.write("Name=Kiosk\n")
#configHandle.write("Exec=/usr/bin/chromium --incognito --start-maximized --no-default-browser-check --kiosk https://remote.knightsbridgeschool.com\n")
#configHandle.close()

#os.system("reboot")
