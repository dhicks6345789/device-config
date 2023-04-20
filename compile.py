import os
import sys

import deviceConfig

for item in os.listdir():
  if item not in ["compile.py", "README.md", "config.py", "__pycache__", ".git", "deviceConfig.py", "LICENSE"]:
    outputFile = sys.argv[1] + "/" + item
    print("DeviceConfig - compiling " + item + " to " + outputFile)
    libText = deviceConfig.readFile("deviceConfig.py")
    outputText = deviceConfig.readFile(item)
    deviceConfig.writeFile(outputFile, outputText.replace("import deviceConfig", libText))
