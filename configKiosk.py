import deviceConfig

def setHostname():
    getSetting("Hostname")
    if not os.uname == getSetting("Hostname"):
        os.system("echo " + getSetting("Hostname") + " > /etc/hostname")

def removeGrubBootTimeout():
    if os.path.exists("/boot/grub/grub.cfg"):
        print("Removing boot timeout from grub.cfg.")
        replaceStringsInFile("/boot/grub/grub.cfg", {"timeout=5":"timeout=0"})

print("Configure system as a Web Kiosk.")

validValueOptions.append("URL")
validValueOptions.append("restartOrShutdown")

print("On startup, load which URL?")
URL = getSetting("URL")

print("On browser exit, shutdown (s) or restart (r)?")
restartOrShutdown = getSetting("restartOrShutdown")
if restartOrShutdown == "s":
    restartOrShutdown = "shutdown now"
else:
    restartOrShutdown = "reboot"

#setHostname()
#removeGrubBootTimeout()

#writeFile("/home/pi/autorun.sh", [
#    "sleep 4",
#    "amixer cset numid=3 1",
#    "/usr/bin/python3 /home/pi/restartServer.py &",
#    chromiumPath + " --incognito --start-maximized --no-default-browser-check --kiosk --disable-popup-blocking --disable-component-update --simulate-outdated-no-au=\"Tue, 31 Dec 2099 23:59:59 GMT\" --user-agent=\"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36\" " + URL + " > /dev/null 2>&1",
#    restartOrShutdown
#])

#writeFile("/var/spool/cron/crontabs/root", [
#    "15 03 * * * /sbin/reboot\n"
#])
#os.system("chmod 0600 /var/spool/cron/crontabs/root")

#setAutostart(["@xset s off","@xset -dpms","@xset s noblank","bash /home/pi/autorun.sh"])
