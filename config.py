#!/usr/bin/python3

# Standard libraries.
import os
import sys
import collections

if os.path.exists("/usr/bin/chromium"):
  chromiumPath = "/usr/bin/chromium"
elif os.path.exists("/usr/bin/chromium-browser"):
  chromiumPath = "/usr/bin/chromium-browser"
else:
  print("Error - Chromium not installed.")
  sys.exit(1)

menu = collections.OrderedDict()
menu["Development Environments"] = collections.OrderedDict()
menu["Development Environments"]["Python with Hugo"] = "pythonHugo"
menu["Development Environments"]["GOV.UK / Jekyll"] = "govukJekyll"

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
    
#menuResult = displayMenu(menu)
#if menuResult == "pythonHugo":
#  print "Configuring system with Python and Hugo..."
#elif menuResult == "govukJekyll":
#  print "Configuring system with the GOV.UK Jekyll environment..."  

#sys.exit(1)

print("Re-writing GUI Autostart file.")
configHandle = open("/etc/xdg/lxsession/LXDE-pi/autostart","w")
configHandle.write("xset s noblank\n")
configHandle.write("xset s off\n")
configHandle.write("xset -dpms\n")
configHandle.write("point-rpi\n")
#configHandle.write(chromiumPath + " --incognito --start-maximized --no-default-browser-check --kiosk https://remote.knightsbridgeschool.com\n")
configHandle.write(chromiumPath + " --incognito --start-maximized --no-default-browser-check --start-fullscreen https://docs.google.com/presentation/d/e/2PACX-1vRstVVaPRpKUAgmU-IIwk4ywY_pzhqynhMqG7BJY8ya4tf_82G01RZL1TqVcLVCBI2xkfYL-oLLUyxB/pub?start=true&loop=true&delayms=6000\n")
configHandle.close()

sys.exit(1)

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
