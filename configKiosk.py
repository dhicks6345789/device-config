import deviceConfig

def setHostname():
    newHostname = getSetting("hostname", "What do you want to call this computer?")
    if not os.uname == newHostname:
        os.system("echo " + newHostname + " > /etc/hostname")

def removeGrubBootTimeout():
    if os.path.exists("/boot/grub/grub.cfg"):
        print("Removing boot timeout from grub.cfg.")
        replaceStringsInFile("/boot/grub/grub.cfg", {"timeout=5":"timeout=0"})

print("Configure system as a Web Kiosk.")

validValueOptions.append("URL")
parseSettings()

URL = getSetting("URL", "On startup, load which URL?")

setHostname()
removeGrubBootTimeout()
runIfPathMissing("/usr/bin/unclutter", "Installing Unclutter, a utility for hiding the mouse cursor.", "apt -y install unclutter")
runIfPathMissing("/usr/bin/xdotool", "Installing XDoTool, a utility for automating XWindows via simulated mouse / keypresses.", "apt -y install xdotool")

# Raspberry Pi OS, as of April 2022, no longer has a default "pi" user, so we can't assume the "/home/pi" home folder exists and have to check and see what
# home folder actually exists. If just the one home folder exists we use that, otherwise we ask which to use. See Raspberry Pi blog for more details:
# https://www.raspberrypi.com/news/raspberry-pi-bullseye-update-april-2022/
homeList = os.listdir("/home")
if len(homeList) == 1:
    userHome = homeList[0]
else:
    userHome = getSetting("userHome", "Which home folder to store autorun.sh in?")
autorunLocation = "/home/" + userHome + "/autorun.sh"

writeFile(autorunLocation, [
    "sleep 4",
    "amixer cset numid=3 1",
    "unclutter -idle 0 &",
    chromiumPath + " --incognito --no-default-browser-check --disable-popup-blocking --disable-component-update &",
    "sleep 15",
    "xdotool type '" + URL + "'",
    "xdotool key Linefeed",
    "sleep 4",
    "xdotool key F11"
])

writeFile("/var/spool/cron/crontabs/root", [
    "15 03 * * * /sbin/reboot\n"
])
os.system("chmod 0600 /var/spool/cron/crontabs/root")

setPiAutostart(["bash " + autorunLocation])
