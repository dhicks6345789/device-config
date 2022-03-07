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
runIfPathMissing("/usr/bin/unclutter", "Installing XDoTool, a utility for automating XWindows via simulated mouse / keypresses.", "apt -y install xdotool")

writeFile("/home/pi/autorun.sh", [
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

setPiAutostart(["bash /home/pi/autorun.sh"])
