import os
import sys

import deviceConfig

for item in os.listdir():
  if item not in ["compile.py"]:
    outputFile = sys.argv[1] + "/" + item
    print("Compiling " + item + " to " + outputFile)
    
    #libText = deviceConfig.readFile("deviceConfig.py")
    #outputText = deviceConfig.readFile(item)
    #deviceConfig.writeFile(outputFile, outputText.replace("import deviceConfig", libText))
