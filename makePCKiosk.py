#!/usr/bin/python3

# Standard libraries.
import os

print("Configuring...")
os.makedirs("/home/pi/.config/autostart", exist_ok=True)
configHandle = open("/home/pi/.config/autostart/kiosk.desktop", "w")
configHandle.write("[Desktop Entry]\n")
configHandle.write("Type=application\n")
configHandle.write("Name=Kiosk\n")
configHandle.write("Exec=/usr/bin/chromium --incognito --start-maximized https://remote.knightsbridgeschool.com\n")
configHandle.close()
