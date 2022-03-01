import os

import device-config

print("STATUS: Compiling " + sys.argv[1] + " to " + sys.argv[2])

libText = device-config.readFile("device-config.py")
outputText = device-config.readFile(sys.argv[1])
device-config.writeFile(sys.argv[2], outputText.replace("import device-config", libText))
