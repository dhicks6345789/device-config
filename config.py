#!/usr/bin/python3

# Standard libraries.
import os
import sys
import collections

chromiumPath = ""
if os.path.exists("/usr/bin/chromium"):
  chromiumPath = "/usr/bin/chromium"
elif os.path.exists("/usr/bin/chromium-browser"):
  chromiumPath = "/usr/bin/chromium-browser"

menu = collections.OrderedDict()
menu["Server Environments"] = collections.OrderedDict()
menu["Server Environments"]["Python with Hugo"] = "pythonHugo"
menu["Server Environments"]["GOV.UK / Jekyll"] = "govukJekyll"
menu["Client Environments"] = collections.OrderedDict()
menu["Client Environments"]["Web-based Kiosk"] = "webKiosk"
menu["Client Environments"]["Science Datalogging Kiosk"] = "dataloggingKiosk"

def displayMenu(theMenu):
  currentItem = 1
  for menuItem in theMenu.keys():
    print(str(currentItem) + ": " + menuItem)
    currentItem = currentItem + 1
  userSelection = input("Selection: ")
  selectedOption = theMenu[list(theMenu.keys())[int(userSelection)-1]]
  if isinstance(selectedOption, collections.OrderedDict):
    return(displayMenu(selectedOption))
  return(selectedOption)

def setAutostart(autostartLines):
  print("Re-writing GUI Autostart file.")
  configHandle = open("/etc/xdg/lxsession/LXDE-pi/autostart","w")
  configHandle.write("xset s noblank\n")
  configHandle.write("xset s off\n")
  configHandle.write("xset -dpms\n")
  configHandle.write("point-rpi\n")
  for autostartLine in autostartLines:
      configHandle.write(autostartLine + "\n")
  #configHandle.write(chromiumPath + " --incognito --start-maximized --no-default-browser-check --kiosk https://remote.knightsbridgeschool.com\n")
  #configHandle.write(chromiumPath + " --incognito --start-maximized --no-default-browser-check --start-fullscreen https://docs.google.com/presentation/d/e/2PACX-1vRstVVaPRpKUAgmU-IIwk4ywY_pzhqynhMqG7BJY8ya4tf_82G01RZL1TqVcLVCBI2xkfYL-oLLUyxB/pub?start=true&loop=true&delayms=6000\n")
  configHandle.close()

def removeGrubBootTimeout():
  if os.path.exists("/boot/grub/grub.cfg"):
    print("Removing boot timeout from grub.conf.")
    configString = ""
    configHandle = open("/boot/grub/grub.cfg")
    for configLine in configHandle.readlines():
      configString = configString + configLine.replace("timeout=5","timeout=0")
    configHandle.close()
    
    configHandle = open("/boot/grub/grub.conf","w")
    configHandle.write(configString)
    configHandle.close()
    
def configRclone():
  print("Configuring rclone...")
    
menuResult = displayMenu(menu)
if menuResult == "pythonHugo":
  print("Configuring system with Python and Hugo...")
elif menuResult == "govukJekyll":
  print("Configuring system with the GOV.UK Jekyll environment...")
elif menuResult == "dataloggingKiosk":
  print("Configuring system as a Science Datalogging Kiosk...")
  removeGrubBootTimeout()
  setAutostart([chromiumPath + " --incognito --start-maximized --no-default-browser-check https://sites.google.com/knightsbridgeschool.com/senior])
  print(" - Install logging software, Chrome")
  print(" - Set up rclone")
  print(" - Hand over to web-editable script to run logging, Chrome, anything else")
