#Name: OctoUpload
#Info: Uploads sliced gcode to OctoPrint server after slicing
#Depend: GCode
#Type: postprocess
#Param: hostIP(string:127.0.0.1) IP Address
#Param: octoPort(string:80) Port
#Param: apiKey(string:enter your api key) API Key
#Param: outputName(string:output) Output Filename
##Param: autoPrint(string:no) Print on upload (yes/no)

#todo
#connect & upload to octo
#option for autostart print
#option to not upload during real time slicing

version = "0.1"
import re

#prints user's input
print hostIP + ":" + octoPort
print apiKey
print outputName
#print autoPrint

#makes a copy of the gcode to send to OctoPrint
with open(filename, "r") as f:

    file = open(outputName + ".gcode", "w")

    gcode = f.readlines()

    file.writelines(gcode)

    file.close()

    #print gcode
