import deviceConfig

print("Configure system as an Exams Machine.")

setHostname()
removeGrubBootTimeout()

autorunLocation = "/home/" + piGetUserHomeFolder() + "/autorun.sh"

#writeFile(autorunLocation, [
#    "sleep 4"
#])

#setPiAutostart(["bash " + autorunLocation])
