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
    print("Removing boot timeout from grub.cfg.")
    configString = ""
    configHandle = open("/boot/grub/grub.cfg")
    for configLine in configHandle.readlines():
      configString = configString + configLine.replace("timeout=5","timeout=0")
    configHandle.close()
    
    configHandle = open("/boot/grub/grub.cfg","w")
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
  if not os.path.exists("linuxSensorlab.zip"):
    os.system("curl -s -o linuxSensorlab.zip \"http://ccgi.dcpmicro.plus.com/dcplogit/files/software/linuxSensorlab.zip\"")
    os.system("unzip linuxSensorlab.zip")
    os.system("gunzip SensorLab\ 1-1-0\ for\ Linux.tgz")
    os.system("tar xf SensorLab\ 1-1-0\ for\ Linux.tar")
    os.system("apt-get install -y libpangox-1.0-0")
    os.system("apt-get install -y libpango1.0-0")
    os.system("curl -s -o libpng12-0.deb \"http://ftp.uk.debian.org/debian/pool/main/libp/libpng/libpng12-0_1.2.50-2+deb8u3_i386.deb\"")
    os.system("dpkg -i libpng12-0.deb")
    os.system("dpkg -i /home/pi/device-config/SensorLab\ 1-1-0\ for\ Linux/Installer/sccresearch-sensorlab_1.1-0_i386.deb")
    os.system("dpkg -i /home/pi/device-config/SensorLab\ 1-1-0\ for\ Linux/Installer/sccresearch-usbrules_1.1-0_all.deb")
  if not os.path.exists("/usr/bin/expect"):
    os.system("apt-get -y install expect")
  if not os.path.exists("/usr/bin/rclone"):
    os.system("curl https://rclone.org/install.sh | bash")
  if not os.path.exists("/home/pi/.config/rclone/rclone.conf"):
    expectFile = open("rclone.expect", "w")
    expectFile.write("\n".join([
      "spawn /usr/bin/rclone config",
      "expect \"n/s/q>\"",
      "send \"n\\r\"",
      "expect \"name>\"",
      "send \"drive\\r\"",
      "expect \"Storage>\"",
      "send \"drive\\r\"",
      "expect \"client_id>\"",
      "send \"556680234914-khamoi3j7tf3d723pe3n9u5ipvnlbsq5.apps.googleusercontent.com\\r\"",
      "expect \"client_secret>\"",
      "send \"FZ-AFSv5AORIroYBf93fvS7v\\r\"",
      "expect \"scope>\"",
      "send \"drive\\r\"",
      "expect \"root_folder_id>\"",
      "send \"\\r\"",
      "expect \"service_account_file>\"",
      "send \"\\r\"",
      "expect \"y/n>\"",
      "send \"n\\r\"",
      "expect \"y/n>\"",
      "send \"y\\r\"",
      "expect \"y/n>\"",
      "send \"n\\r\"",
      "expect \"y/e/d>\"",
      "send \"y\\r\"",
      
      "expect \"e/n/d/r/c/s/q>\"",
      "send \"n\\r\"",
      "expect \"name>\"",
      "send \"Documents\\r\"",
      "expect \"Storage>\"",
      "send \"cache\\r\"",
      "expect \"remote>\"",
      "send \"drive:\\r\"",
      "expect \"plex_url>\"",
      "send \"\\r\"",
      "expect \"plex_username>\"",
      "send \"\\r\"",
      "expect \"y/g/n>\"",
      "send \"n\\r\"",
      "expect \"chunk_size>\"",
      "send \"10M\\r\"",
      "expect \"info_age>\"",
      "send \"1y\\r\"",
      "expect \"chunk_total_size>\"",
      "send \"1G\\r\"",
      "expect \"y/n>\"",
      "send \"n\\r\"",
      "expect \"y/e/d>\"",
      "send \"y\\r\"",
      "expect \"e/n/d/r/c/s/q>\"",
      "send \"q\\r\""
    ]))
    
    expectFile.close()
    os.system("su pi -c \"expect rclone.expect\"")
    os.system("rm rclone.expect")
    
  print("Set boot process to hand over to web-editable script (owned by the datalogging user) to run logging software, Chrome, or anything else needed.")
  autorunFile = open("/home/pi/autorun.sh", "w")
  autorunFile.write("\n".join([
    "sleep 10",
    "/usr/bin/rclone mount --allow-non-empty --allow-other --vfs-cache-mode full --vfs-cache-max-age 999h --config=/home/pi/.config/rclone/rclone.conf Documents:Datalogging /home/pi/Documents > /tmp/rclone.log 2>&1 &",
    "curl -L -s \"https://drive.google.com/uc?export=download&id=1UxZMVK_YfD_B2fC_XlGfPaIKeV9T6yVp\" | python3"
  ]))
  autorunFile.close()
  setAutostart(["bash /home/pi/autorun.sh"])
