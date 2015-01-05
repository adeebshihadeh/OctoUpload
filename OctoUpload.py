#Name: OctoUpload
#Info: Uploads gcode to OctoPrint server after slicing (All fields required)
#Depend: GCode
#Type: postprocess
#Param: hostIP(string:octopi.local) IP Address
#Param: hostPort(string:80) Port
#Param: apiKey(string:156A8AE4000940CFB3C51C9DFD812D8A) API Key
#Param: outputName(string:output) Output Filename
##Param: autoPrint(string:no) Print on upload (yes/no)

#todo
#connect & upload to octo
#option for autostart print
#option to not upload during real time slicing
#option for different variations of gcode (.gcode, .gco, .g)
#get model name & set as output

version = "0.1"

import cookielib
import socket
import urllib
import urllib2
import json

myGcode = outputName
myKey = apiKey

#prints user's input
print "IP: " + hostIP + ":" + hostPort
print "API key: " + apiKey
print "Filename: " + myGcode + ".gcode"
#print autoPrint

#makes a copy of the gcode to send to OctoPrint
with open(filename, "r") as f:

    file = open(myGcode + ".gcode", "w")

    gcode = f.readlines()

    file.writelines(gcode)

    file.close()

    #print gcode

#this is for urlib2
url = "http://" + hostIP + ":" + hostPort + "/api/files/local"
print "URL: " + url

http_header = {
                #"User-Agent" : "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36",
                #"Host" : hostIP,
                #"Accept" : "application/json, text/javascript,*/*;q=0.01",
                #"Accept-Encoding" : "gzip, deflate",
                #"X-Requested-With" : "XMLHttpRequest",
                #"Content-Type": "multipart/form-data; boundary=----WebKitFormBoundaryDeC2E3iWbTv1PwMC",
                #"Content-Type" : "multipart/form-data",
                "Content-Type" : "form-data",
                "X-Api-Key" : myKey
                }
payload = {
    "Content-Disposition" : "form-data; name='file'; filename='output.gcode'",
    "Content-Type" : "application/octet-stream",
    'file': open(myGcode + ".gcode", 'rb').readlines()
}

files = {
    'file': open(myGcode + ".gcode", 'rb'),
    "filename" : "octoupload" + ".gcode"
}

# setup socket connection timeout
timeout = 15
socket.setdefaulttimeout(timeout)

# create an urllib2 opener()
opener = urllib2.build_opener(urllib2.HTTPHandler(debuglevel=1))

# create your HTTP request
req = urllib2.Request(url, urllib.urlencode(payload), http_header)
print req
print "Uploading..."

# submit your request
#res = opener.open(req)
feeddata = opener.open(req).read()
# html = res.read()
# print html
# response = urllib2.urlopen(req)
#
# print "Response: " + response

# save retrieved HTML to file
# open("tmp.html", "w").write(html)
# print "HTML" + html

print "done"
