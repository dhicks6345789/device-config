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

# Reads the given file, returns the entire contents as a single string.
def readFile(theFilename):
    inHandle = open(theFilename, encoding="latin-1")
    result = inHandle.read()
    inHandle.close()
    return result

# Write a file. Takes a file path and either a single string or an array of strings.
# If an array, will write each string to the given file path with a newline at the end.
def writeFile(theFilename, theFileData):
    fileDataHandle = open(theFilename, "w")
    if isinstance(theFileData, str):
        fileDataHandle.write(theFileData)
    else:
        for dataLine in theFileData:
            fileDataHandle.write(dataLine + "\n")
    fileDataHandle.close()

# Reads the given file, replaces any strings found in the given dict with their
# replacement, then rew-writes the result to the file.
def replaceStringsInFile(theFilename, theReplaceDict):
    textFileContents = readFile(theFilename)
    for findValue in theReplaceDict.keys():
        textFileContents = textFileContents.replace(findValue, theReplaceDict[findValue])
    write(theFilename, textFileContents)

# If the given path does not exist, print the given message and run the given command.
def runIfPathMissing(thePath, theMessage, theCommand):
    if not os.path.exists(thePath):
        if not theMessage == "":
            print(theMessage)
        os.system(theCommand)

validBooleanOptions = []
validValueOptions = []
settings = {}
# Parse any options set by the user on the command line.
def parseSettings():
    optionCount = 1
    while optionCount < len(sys.argv):
        if sys.argv[optionCount].startswith("--"):
            argName = sys.argv[optionCount][2:]
            if argName in validBooleanOptions:
                settings[argName] = True
            elif argName in validValueOptions:
                settings[argName] = sys.argv[optionCount+1]
                optionCount = optionCount + 1
            else:
                print("ERROR: Invalid argument given: " + argName)
                sys.exit(1)
        else:
            print("ERROR: Orphaned value given: " + sys.argv[optionCount])
            sys.exit(1)
        optionCount = optionCount + 1

def getSetting(theSetting, theMessage):
    if not theSetting in settings.keys():
        print(theMessage)
        settings[theSetting] = input(theSetting + ": ")
    return(settings[theSetting])

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

# Make sure Expect (a system automation tool) is installed.
def installExpect():
    if not os.path.exists("/usr/bin/expect"):
        print("Installing Expect...")
        os.system("apt-get -y install expect")

# Write the given array of strings to a temporary file and run that file as an Expect script.
# Removes the temporary file afterwards.
def runExpect(inputArray):
    writeFileFromArray("temp.expect", inputArray)
    os.system("su pi -c \"expect temp.expect\"")
    os.system("rm temp.expect")

# A function to write the LXDE autostart file on the Raspberry Pi to run the given command lines, given as an array of strings.
def setPiAutostart(autostartLines):
    print("Re-writing GUI Autostart file.")
    writeFile("/etc/xdg/lxsession/LXDE-pi/autostart", [
        "# @lxpanel --profile LXDE-pi",
        "# @pcmanfm --desktop --profile LXDE-pi",
        "# @xscreensaver -no-splash",
        "xset s noblank",
        "xset s off",
        "xset -dpms",
        "point-rpi"
    ] + autostartLines)
    
# Make sure RClone (a cloud file access utility) is installed.
def installRclone():
    if not os.path.exists("/usr/bin/rclone"):
        print("Installing rclone...")
        os.system("curl https://rclone.org/install.sh | bash")

# Automate RClone's configuration.
# To-do: add more options so caller can add storage.
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
        
def setHostname():
    newHostname = getSetting("hostname", "What do you want to call this computer?")
    if not os.uname == newHostname:
        os.system("echo " + newHostname + " > /etc/hostname")

def removeGrubBootTimeout():
    if os.path.exists("/boot/grub/grub.cfg"):
        print("Removing boot timeout from grub.cfg.")
        replaceStringsInFile("/boot/grub/grub.cfg", {"timeout=5":"timeout=0"})

# Raspberry Pi OS, as of April 2022, no longer has a default "pi" user, so we can't assume the "/home/pi" home folder exists and have to check and see what
# home folder actually exists. If just the one home folder exists we use that, otherwise we ask which to use. See Raspberry Pi blog for more details:
# https://www.raspberrypi.com/news/raspberry-pi-bullseye-update-april-2022/
def piGetUserHomeFolder():
    homeList = os.listdir("/home")
    if len(homeList) == 1:
        userHome = homeList[0]
    else:
        userHome = getSetting("userHome", "Which home folder to store autorun.sh in?")
    return(userHome)
