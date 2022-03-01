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
validValueOptions.append("restartOrShutdown")
parseSettings()

URL = getSetting("URL", "On startup, load which URL?")
restartOrShutdown = getSetting("restartOrShutdown", "On browser exit, shutdown (s) or restart (r)?")
if restartOrShutdown == "s":
    restartOrShutdown = "shutdown now"
elif restartOrShutdown == "r":
    restartOrShutdown = "reboot"
else:
    restartOrShutdown = ""

setHostname()
removeGrubBootTimeout()
runIfPathMissing("/usr/bin/unclutter", "Installing Unclutter, a utility for hiding the mouse cursor.", "apt -y install unclutter")

writeFile("/home/pi/autorun.sh", [
    "sleep 4",
    "amixer cset numid=3 1",
    "unclutter -idle 0 &",
    chromiumPath + " --incognito --start-maximized --no-default-browser-check --kiosk --disable-popup-blocking --disable-component-update --simulate-outdated-no-au=\"Tue, 31 Dec 2099 23:59:59 GMT\" --user-agent=\"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36\" " + URL + " > /dev/null 2>&1",
    restartOrShutdown
])

writeFile("/var/spool/cron/crontabs/root", [
    "15 03 * * * /sbin/reboot\n"
])
os.system("chmod 0600 /var/spool/cron/crontabs/root")

#setPiAutostart(["@xset s off","@xset -dpms","@xset s noblank","bash /home/pi/autorun.sh"])
setPiAutostart(["bash /home/pi/autorun.sh"])
