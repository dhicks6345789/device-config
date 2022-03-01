import sys

import deviceConfig

print("Compiling " + sys.argv[1] + " to " + sys.argv[2])

libText = deviceConfig.readFile("deviceConfig.py")
outputText = deviceConfig.readFile(sys.argv[1])
deviceConfig.writeFile(sys.argv[2], outputText.replace("import deviceConfig", libText))
