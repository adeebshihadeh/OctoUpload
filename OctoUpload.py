#Name: OctoUpload
#Info: Uploads gcode to OctoPrint server after slicing
#Depend: GCode
#Type: postprocess
#Param: hostIP(string:) IP Address
#Param: octoPort(string:80) Port
#Param: apiKey(string:) API Key
#Param: outputName(string:output) Output Filename
#Param: sendLoc(string:local) OctoPrint Location (local or sdcard)
#Param: gcodeExt(string:gcode) GCode Extension
##Param: autoPrint(string:no) Print on upload (yes/no)

# todo
# 1. Automatically figure out a default filename based on first STL loaded
# 2. Create a checkmark for SSL vs Non-SSL
# 3. Optional Settings (ideally a expand/hidey thing) for octoPort, outputName (Optional because See #1), and basic auth username/password

version = "0.1"

import base64
import socket
import urllib
import urllib2
import mimetools

timeout = 15
socket.setdefaulttimeout(timeout)

print hostIP
print octoPort
print apiKey
print outputName
print sendLoc
print gcodeExt

#remove extension user may have used on the filename
outputName = outputName.split(".")[0]
print outputName

#remove . user may have used on extension
if gcodeExt.find(".") != -1:
    gcodeExt = gcodeExt.split(".")[1]
    print gcodeExt

#add extension user specifies
if gcodeExt == "g":
    outputName = outputName + "." + gcodeExt
elif gcodeExt == "gco":
    outputName = outputName + "." + gcodeExt
else:
    outputName = outputName + ".gcode"
print "Ext: " + outputName

username = "spec"
password = "password"

#sends the gcode to either sd or local
if sendLoc == "sdcard":
    url = "http://" + hostIP + ":" + octoPort + "/api/files/sdcard"
else:
    url = "http://" + hostIP + ":" + octoPort + "/api/files/local"

filebody = open(filename, 'rb').read()
mimetype = 'application/octet-stream'
boundary = mimetools.choose_boundary()
content_type = 'multipart/form-data; boundary=%s' % boundary

body = []
body_boundary = '--' + boundary
body = [  body_boundary,
          'Content-Disposition: form-data; name="file"; filename="%s"' % outputName,
          'Content-Type: %s' % mimetype,
          '',
          filebody,
      ]

body.append('--' + boundary + '--')
body.append('')
body = '\r\n'.join(body)

req = urllib2.Request(url)
# Uncomment below two lines for basic auth support. (Used in cases where haproxy is in front of octoprint, with basic auth enabled).
#base64string = base64.encodestring('%s:%s' % (username, password))
#req.add_header("Authorization", "Basic %s" % base64string)
req.add_header('User-agent', 'Cura AutoUploader Plugin')
req.add_header('Content-type', content_type)
req.add_header('Content-length', len(body))
req.add_header('X-Api-Key', apiKey)
req.add_data(body)

print "Uploading..."
print urllib2.urlopen(req).read()
print "Done"
