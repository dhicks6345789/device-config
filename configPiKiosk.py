import deviceConfig

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
