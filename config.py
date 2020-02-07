#!/usr/bin/python3

# Standard libraries.
import os
import sys
import collections

settings = {}

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
menu["Client Environments"]["Datalogging Machine"] = "dataloggingMachine"
menu["Client Environments"]["Web Browsing Machine"] = "webBrowsingMachine"
menu["Client Environments"]["Exam Clock"] = "examClock"

def getSetting(theSetting):
  if not theSetting in settings.keys():
    settings[theSetting] = input(theSetting + ": ")
  return(settings[theSetting])

def setHostname():
  getSetting("Hostname")
  if not os.uname == getSetting("Hostname"):
    os.system("echo " + getSetting("Hostname") + " > /etc/hostname")
    
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

def replaceStringsInFile(theFilename, theReplaceArray):
  textFile = open(theFilename, encoding="latin-1")
  textFileContents = textFile.read()
  textFile.close()
  for findValue in theReplaceArray.keys():
    textFileContents = textFileContents.replace(findValue, theReplaceArray[findValue])
  textFile = open(theFilename, "w")
  textFile.write(textFileContents)
  textFile.close()

# Note: this doesn't actually seem to work - setting gets set back on reboot. Added --disable-popup-blocking to Chromium instead.
# Suspect the "last updated" field needs changing.
def setAllowedPopupURLs():
  replaceStringsInFile("/home/pi/.config/chromium/Default/Preferences", {"\"popups\":{}":"\"popups\":{\"knightsbridgeschool.isams.cloud,*\":{\"last_modified\":\"13214925214214283\",\"setting\":1}}"})
  
def setAutostart(autostartLines):
  print("Re-writing GUI Autostart file.")
  writeFileFromArray("/etc/xdg/lxsession/LXDE-pi/autostart", [
    "xset s noblank"
    "xset s off"
    "xset -dpms"
    "point-rpi"
  ] + autostartLines)
  
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
    
def readFile(theFilename):
  inputFile = open(theFilename)
  result = inputFile.read()
  inputFile.close()
  return result
    
def writeFileFromArray(theFilename, theArray):
  outputFile = open(theFilename, "w")
  outputFile.write("\n".join(theArray))
  outputFile.close()
    
def runExpect(inputArray):
  writeFileFromArray("temp.expect", inputArray)
  os.system("su pi -c \"expect temp.expect\"")
  os.system("rm temp.expect")
  
def installSensorLab():
  if not os.path.exists("/usr/share/sccresearch-sensorlab"):
    print("Installing SensorLab...")
    os.system("curl -s -o linuxSensorlab.zip \"http://ccgi.dcpmicro.plus.com/dcplogit/files/software/linuxSensorlab.zip\"")
    os.system("unzip linuxSensorlab.zip")
    os.system("gunzip SensorLab\ 1-1-0\ for\ Linux.tgz")
    os.system("tar xf SensorLab\ 1-1-0\ for\ Linux.tar")
    os.system("apt-get install -y libpangox-1.0-0")
    os.system("apt-get install -y libpango1.0-0")
    os.system("curl -s -o libpng12-0.deb \"http://ftp.uk.debian.org/debian/pool/main/libp/libpng/libpng12-0_1.2.50-2+deb8u3_i386.deb\"")
    os.system("dpkg -i libpng12-0.deb")
    os.system("dpkg -i SensorLab\ 1-1-0\ for\ Linux/Installer/sccresearch-sensorlab_1.1-0_i386.deb")
    os.system("dpkg -i SensorLab\ 1-1-0\ for\ Linux/Installer/sccresearch-usbrules_1.1-0_all.deb")
    os.system("rm linuxSensorlab.zip")
    os.system("rm libpng12-0.deb")
    os.system("rm SensorLab\ 1-1-0\ for\ Linux.tar")
    os.system("rm -rf SensorLab\ 1-1-0\ for\ Linux")
    
def configRclone():
  if not os.path.exists("/usr/bin/expect"):
    print("Installing Expect...")
    os.system("apt-get -y install expect")
  if not os.path.exists("/usr/bin/rclone"):
    print("Installing rclone...")
    os.system("curl https://rclone.org/install.sh | bash")
  if not os.path.exists("/home/pi/.config/rclone/rclone.conf"):
    print("Configuring rclone...")
    runExpect([
      "spawn /usr/bin/rclone config",
      "expect \"n/s/q>\"",
      "send \"n\\r\"",
      "expect \"name>\"",
      "send \"drive\\r\"",
      "expect \"Storage>\"",
      "send \"drive\\r\"",
      "expect \"client_id>\"",
      "send \".apps.googleusercontent.com\\r\"",
      "expect \"client_secret>\"",
      "send \"\\r\"",
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
    ])
  
menuResult = displayMenu(menu)
if menuResult == "pythonHugo":
  print("Configuring system with Python and Hugo...")
elif menuResult == "govukJekyll":
  print("Configuring system with the GOV.UK Jekyll environment...")
elif menuResult == "webKisok":
  print("Configuring system as a Web Kiosk...")
  #configHandle.write(chromiumPath + " --incognito --start-maximized --no-default-browser-check --kiosk https://something.example.com\n")
elif menuResult == "dataloggingMachine":
  print("Configuring system as a Datalogging Machine...")
  setHostname()
  removeGrubBootTimeout()
  installSensorLab()
  configRclone()
  
  print("Set up process to move any files we find stored in the local /home/pi folder to the mounted network /home/pi/Documents folder.")
  os.system("curl -L -s -o /home/pi/moveFiles.py \"https://drive.google.com/uc?export=download&id=1PpFJIwShCxy3O--jaKEGQyjzHlr0xclA\"")
    
  print("Set boot process to hand over to web-editable script (owned by the datalogging user) to run logging software, Chrome, or anything else needed.")
  writeFileFromArray("/home/pi/autorun.sh", [
    "sleep 10",
    "/usr/bin/rclone mount --allow-non-empty --vfs-cache-mode full --vfs-cache-max-age 999h --config=/home/pi/.config/rclone/rclone.conf Documents:Datalogging/" + newHostname + " /home/pi/Documents > /tmp/rclone.log 2>&1 &",
    "python3 /home/pi/moveFiles.py &",
    "curl -L -s \"https://drive.google.com/uc?export=download&id=1UxZMVK_YfD_B2fC_XlGfPaIKeV9T6yVp\" | python3"
  ])
  setAutostart(["bash /home/pi/autorun.sh"])
elif menuResult == "webBrowsingMachine":
  print("Configuring system as a Web Browsing Machine...")
  setHostname()
  removeGrubBootTimeout()
  print("On startup, load which URL?")
  URL = getSetting("URL")
  print("On browser exit, shutdown (s) or restart (r)?")
  restartOrShutdown = getSetting("restartOrShutdown")
  if restartOrShutdown == "s":
    restartOrShutdown = "shutdown now"
  else:
    restartOrShutdown = "reboot"
    
  writeFileFromArray("/home/pi/restartServer.py", [
    "import os",
    "import http.server",
    "",
    "class restartServer(http.server.BaseHTTPRequestHandler):",
    "  def do_GET(self):",
    "    self.send_response(200)",
    "    self.send_header('Content-type', 'text/html')",
    "    self.send_header('Access-Control-Allow-Origin', '*')",
    "    self.end_headers()",
    "    if self.path == '/restart':",
    "      os.system('reboot')",
    "    elif self.path == '/checkRestart':",
    "      self.wfile.write('restartPresent'.encode('utf-8'))",
    "    else:",
    "      self.wfile.write('Nothing to do.'.encode('utf-8'))",
    "",
    "httpd = http.server.HTTPServer(('127.0.0.1', 8000), restartServer)",
    "httpd.serve_forever()"
  ])
  
  inApplications = False
  output = []
  for rcDataLine in readFile("/etc/xdg/openbox/lxde-pi-rc.xml").split("\n"):
    if rcDataLine.strip() == "<titleLayout>LIMC</titleLayout>":
      rcDataLine = "    <titleLayout>C</titleLayout>\n"
    if rcDataLine.strip() == "<applications>":
      inApplications = True
      output.append("  <applications>")
      output.append("    <application name=\"panel\">")
      output.append("      <skip_taskbar>yes</skip_taskbar>")
      output.append("      <layer>above</layer>")
      output.append("      </application>")
      output.append("      <application name=\"panel\" type=\"dock\">")
      output.append("      <layer>below</layer>")
      output.append("    </application>")
      output.append("    <application role=\"browser\">")
      output.append("      <fullscreen>yes</fullscreen>")
      output.append("    </application>")
      output.append("  </applications>")
    if not inApplications:
      output.append(rcDataLine)
    if rcDataLine.strip() == "</applications>":
      inApplications = False
  writeFileFromArray("/etc/xdg/openbox/lxde-pi-rc.xml", output)
  
  writeFileFromArray("/home/pi/autorun.sh", [
    "sleep 4",
    "amixer cset numid=3 1",
    "/usr/bin/python3 /home/pi/restartServer.py &",
    chromiumPath + " --incognito --start-maximized --no-default-browser-check --disable-popup-blocking --load-extension=/home/pi/device-config/singleWindow " + URL + " > /dev/null 2>&1",
    restartOrShutdown
  ])
  
  writeFileFromArray("/var/spool/cron/crontabs/root", [
    "15 03 * * * reboot\n"
  ])
  os.system("chmod 0600 /var/spool/cron/crontabs/root")
  
  setAutostart(["@xset s off","@xset -dpms","@xset s noblank","bash /home/pi/autorun.sh"])
elif menuResult == "examClock":
  print("Configuring system as an Exam Clock...")
  removeGrubBootTimeout()
  os.system("apt-get install -y dclock")
  os.system("apt-get install -y xdotool")
  os.system("apt-get install -y wmctrl")
  writeFileFromArray("/home/pi/autorun.sh", [
    "sleep 4",
    "(dclock -seconds -noblink -bg black -led_off black; shutdown now) &",
    "sleep 4",
    "xdotool search --name dclock windowactivate -sync; wmctrl -r :ACTIVE: -b toggle,maximized_vert,maximized_horz"
  ])
  setAutostart(["bash /home/pi/autorun.sh"])
  os.system("reboot")
