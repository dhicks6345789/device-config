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
menu["Server Environments"]["Jamstack for Hugo"] = "jamstackHugo"
menu["Server Environments"]["Jamstack for GOV.UK"] = "jamstackGovuk"
menu["Client Environments"] = collections.OrderedDict()
menu["Client Environments"]["Web-based Kiosk"] = "webKiosk"
menu["Client Environments"]["Datalogging Machine"] = "dataloggingMachine"
menu["Client Environments"]["Web Browsing Machine"] = "webBrowsingMachine"
menu["Client Environments"]["Exam Clock"] = "examClock"

# Parse any options set by the user on the command line.
validBooleanOptions = []
validValueOptions = ["-domainName", "-contentFolderPath", "-jekyllFolderPath"]
settings = {}
optionCount = 1
while optionCount < len(sys.argv):
	if sys.argv[optionCount] in validBooleanOptions:
		settings[sys.argv[optionCount]] = True
	elif sys.argv[optionCount] in validValueOptions:
		settings[sys.argv[optionCount]] = sys.argv[optionCount+1]
		optionCount = optionCount + 1
	optionCount = optionCount + 1

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
	
def runIfPathMissing(thePath, theMessage, theCommand):
	if not os.path.exists(thePath):
		if not theMessage == "":
			print(theMessage)
		os.system(theCommand)
		
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
		
def installExpect():
	if not os.path.exists("/usr/bin/expect"):
		print("Installing Expect...")
		os.system("apt-get -y install expect")
		
def installRclone():
	if not os.path.exists("/usr/bin/rclone"):
		print("Installing rclone...")
		os.system("curl https://rclone.org/install.sh | bash")

def configRclone():
	# Make sure Rclone is set up to connect to the user's cloud storage - we might need to ask the user for some details.
	if not os.path.exists("/root/.config/rclone/rclone.conf"):
		print("Configuring rclone...")
		getSetting("-contentFolderPath", "Please enter the Google Drive path that contains the content")
		getSetting("-jekyllFolderPath", "Please enter the Google Drive path that contains the Jekyll setup")
		runExpect([
			"spawn /usr/bin/rclone config",
			"expect \"n/s/q>\"",
			"send \"n\\r\"",
			"expect \"name>\"",
			"send \"drive\\r\"",
			"expect \"Storage>\"",
			"send \"drive\\r\"",
			"expect \"client_id>\"",
			"expect_user -timeout 3600 -re \"(.*)\\n\"",
			"send \"$expect_out(1,string)\\r\"",
			"expect \"client_secret>\"",
			"expect_user -timeout 3600 -re \"(.*)\\n\"",
			"send \"$expect_out(1,string)\\r\"",
			"expect \"scope>\"",
			"send \"drive.readonly\\r\"",
			"expect \"root_folder_id>\"",
			"send \"\\r\"",
			"expect \"service_account_file>\"",
			"send \"\\r\"",
			"expect \"y/n>\"",
			"send \"n\\r\"",
			"expect \"y/n>\"",
			"send \"n\\r\"",
			"expect \"Enter verification code>\"",
			"expect_user -timeout 3600 -re \"(.*)\\n\"",
			"send \"$expect_out(1,string)\\r\"",
			"expect \"y/n>\"",
			"send \"n\\r\"",
			"expect \"y/e/d>\"",
			"send \"y\\r\"",
			
			"expect \"e/n/d/r/c/s/q>\"",
			"send \"n\\r\"",
			"expect \"name>\"",
			"send \"content\\r\"",
			"expect \"Storage>\"",
			"send \"cache\\r\"",
			"expect \"remote>\"",
			"send \"drive:"+userOptions["-contentFolderPath"]+"\\r\"",
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
			"send \"n\\r\"",
			"expect \"name>\"",
			"send \"jekyll\\r\"",
			"expect \"Storage>\"",
			"send \"cache\\r\"",
			"expect \"remote>\"",
			"send \"drive:"+userOptions["-jekyllFolderPath"]+"\\r\"",
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
			
			"send \"q\\r\""
		])

def installCaddy():
	runIfPathMissing("/usr/bin/caddy", "Installing Caddy (web server)...", "echo \"deb [trusted=yes] https://apt.fury.io/caddy/ /\" | sudo tee -a /etc/apt/sources.list.d/caddy-fury.list; apt-get update; apt-get install caddy")
	
def installJekyll():
	# Make sure Jekyll (static site generation tool) is installed.
	runIfPathMissing("/usr/local/bin/jekyll", "Installing Jekyll (static site generator)...", "gem install bundler jekyll concurrent-ruby")
	runIfPathMissing("/root/.bundle", "", "bundle install")
	os.system("mkdir /.bundle > /dev/null 2>&1")
	#os.system("chown www-data:www-data /.bundle > /dev/null 2>&1")
	
menuResult = displayMenu(menu)
if menuResult == "jamstackHugo":
	print("Configuring system with Jamstack for Hugo...")
elif menuResult == "jamstackGovuk":
	print("Configuring system with Jamstack for GOV.UK...")
	installCaddy()
	installExpect()
	installRclone()
	configRclone()
	#installJekyll()
elif menuResult == "webKiosk":
	print("Configuring system as a Web Kiosk...")	
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
		
	writeFileFromArray("/home/pi/autorun.sh", [
		"sleep 4",
		"amixer cset numid=3 1",
		"/usr/bin/python3 /home/pi/restartServer.py &",
		chromiumPath + " --incognito --start-maximized --no-default-browser-check --kiosk --disable-popup-blocking --disable-component-update --simulate-outdated-no-au=\"Tue, 31 Dec 2099 23:59:59 GMT\" --user-agent=\"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36\" " + URL + " > /dev/null 2>&1",
		restartOrShutdown
	])
	
	writeFileFromArray("/var/spool/cron/crontabs/root", [
		"15 03 * * * /sbin/reboot\n"
	])
	os.system("chmod 0600 /var/spool/cron/crontabs/root")
			
	setAutostart(["@xset s off","@xset -dpms","@xset s noblank","bash /home/pi/autorun.sh"])
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
		"	def do_GET(self):",
		"		self.send_response(200)",
		"		self.send_header('Content-type', 'text/html')",
		"		self.send_header('Access-Control-Allow-Origin', '*')",
		"		self.end_headers()",
		"		if self.path == '/restart':",
		"			os.system('reboot')",
		"		elif self.path == '/checkRestart':",
		"			self.wfile.write('restartPresent'.encode('utf-8'))",
		"		else:",
		"			self.wfile.write('Nothing to do.'.encode('utf-8'))",
		"",
		"httpd = http.server.HTTPServer(('127.0.0.1', 8000), restartServer)",
		"httpd.serve_forever()"
	])
	
	inApplications = False
	output = []
	for rcDataLine in readFile("/etc/xdg/openbox/lxde-pi-rc.xml").split("\n"):
		if rcDataLine.strip().startswith("<titleLayout>"):
			rcDataLine = "		<titleLayout>LMC</titleLayout>\n"
		if rcDataLine.strip() == "<applications>":
			inApplications = True
			output.append("	<applications>")
			output.append("		<application name=\"panel\">")
			output.append("			<skip_taskbar>yes</skip_taskbar>")
			output.append("			<layer>above</layer>")
			output.append("			</application>")
			output.append("			<application name=\"panel\" type=\"dock\">")
			output.append("			<layer>below</layer>")
			output.append("		</application>")
			output.append("		<application role=\"browser\">")
			output.append("			<fullscreen>yes</fullscreen>")
			output.append("		</application>")
			output.append("		<application role=\"pop-up\">")
			output.append("			<fullscreen>no</fullscreen>")
			output.append("		</application>")
			output.append("	</applications>")
		if not inApplications:
			output.append(rcDataLine)
		if rcDataLine.strip() == "</applications>":
			inApplications = False
	writeFileFromArray("/etc/xdg/openbox/lxde-pi-rc.xml", output)
	
	writeFileFromArray("/home/pi/autorun.sh", [
		"sleep 4",
		"amixer cset numid=3 1",
		"/usr/bin/python3 /home/pi/restartServer.py &",
		chromiumPath + " --incognito --start-maximized --no-default-browser-check --disable-popup-blocking --disable-component-update --simulate-outdated-no-au=\"Tue, 31 Dec 2099 23:59:59 GMT\" --user-agent=\"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36\" " + URL + " > /dev/null 2>&1",
		restartOrShutdown
	])
	
	writeFileFromArray("/var/spool/cron/crontabs/root", [
		"15 03 * * * /sbin/reboot\n"
	])
	os.system("chmod 0600 /var/spool/cron/crontabs/root")
	
	os.system("apt-get install -y cups")
	os.system("/etc/init.d/cups stop")
	writeFileFromArray("/etc/cups/printers.conf", [
		"# Printer configuration file for CUPS v2.2.10",
		"# Written by cupsd",
		"# DO NOT EDIT THIS FILE WHEN CUPSD IS RUNNING",
		"<Printer STAFFROOM1>",
		"UUID urn:uuid:0efb25f1-13ee-38b5-63e1-0b504cbc5eb1",
		"Info RICOH MP C5503",
		"Location Staffroom",
		"MakeModel Ricoh MP C5503 - CUPS+Gutenprint v5.3.1",
		"DeviceURI socket://192.168.4.20",
		"State Idle",
		"StateTime 1582551271",
		"ConfigTime 1582551206",
		"Type 12380",
		"Accepting Yes",
		"Shared No",
		"JobSheets none none",
		"QuotaPeriod 0",
		"PageLimit 0",
		"KLimit 0",
		"OpPolicy default",
		"ErrorPolicy retry-job",
		"Attribute marker-colors \#000000,none,#00FFFF,#FF00FF,#FFFF00",
		"Attribute marker-levels 90,0,90,80,30",
		"Attribute marker-names Black Toner,Waste Toner,Cyan Toner,Magenta Toner,Yellow Toner",
		"Attribute marker-types toner,waste-toner,toner,toner,toner",
		"Attribute marker-change-time 1582551271",
		"</Printer>",
		"<Printer STAFFROOM2>",
		"UUID urn:uuid:9d40e26f-8618-3d08-4661-8e904ecc90fc",
		"Info RICOH MP C5503",
		"Location Staffroom",
		"MakeModel Ricoh MP C5503 - CUPS+Gutenprint v5.3.1",
		"DeviceURI socket://192.168.4.10",
		"State Idle",
		"StateTime 1582551279",
		"ConfigTime 1582551144",
		"Type 12380",
		"Accepting Yes",
		"Shared No",
		"JobSheets none none",
		"QuotaPeriod 0",
		"PageLimit 0",
		"KLimit 0",
		"OpPolicy default",
		"ErrorPolicy retry-job",
		"Attribute marker-colors \#000000,none,#00FFFF,#FF00FF,#FFFF00",
		"Attribute marker-levels 80,0,50,70,90",
		"Attribute marker-names Black Toner,Waste Toner,Cyan Toner,Magenta Toner,Yellow Toner",
		"Attribute marker-types toner,waste-toner,toner,toner,toner",
		"Attribute marker-change-time 1582551279",
		"</Printer>"
	])
	os.system("/etc/init.d/cups start")
		
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
