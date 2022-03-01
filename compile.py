import sys

import deviceConfig

print("STATUS: Compiling " + sys.argv[1] + " to " + sys.argv[2])

libText = deviceConfig.readFile("deviceConfig.py")
outputText = deviceConfig.readFile(sys.argv[1])
device-config.writeFile(sys.argv[2], outputText.replace("import deviceConfig", libText))
