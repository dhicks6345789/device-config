#!/usr/bin/python3

# Standard libraries.
import os
import sys
import collections

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
		
# Reads the given file, returns the entire contents as a single string.
def readFile(theFilename):
	inHandle = open(theFilename)
	result = inHandle.read()
	inHandle.close()
	return result

# Handy utility function to write a file. Takes a file path and either a single string or an array of strings. If an array, will write each
# string to the given file path with a newline at the end.
def writeFile(theFilename, theFileData):
	fileDataHandle = open(theFilename, "w")
	if isinstance(theFileData, str):
		fileDataHandle.write(theFileData)
	else:
		for dataLine in theFileData:
			fileDataHandle.write((str(dataLine) + "\n").encode())
	fileDataHandle.close()

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
