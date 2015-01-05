#Name: OctoUpload
#Info: Uploads gcode to OctoPrint server after slicing
#Depend: GCode
#Type: postprocess
#Param: hostIP(string:192.168.140) IP Address
#Param: octoPort(string:80) Port
#Param: apiKey(string:156A8AE4000940CFB3C51C9DFD812D8A) API Key
#Param: outputName(string:output) Output Filename
##Param: autoPrint(string:no) Print on upload (yes/no)

#todo
#connect & upload to octo
#option for autostart print
#option to not upload during real time slicing

version = "0.1"
import re

#import requests

import cookielib
import socket
import urllib
import urllib2
import json

#prints user's input
print hostIP + ":" + octoPort
#print apiKey
#print outputName
#print autoPrint

#makes a copy of the gcode to send to OctoPrint
with open(filename, "r") as f:

    file = open(outputName + ".gcode", "w")

    gcode = f.readlines()

    file.writelines(gcode)

    file.close()

    #print gcode

# url = "http://" + hostIP + "/api/files/local"
# headers = {"content-type" : "form-data"}
# #headers = {"content-type" : "multipart/form-data"}
# X-Api-Key = apiKey
# payload = "path to gcode"
# files = {'file': open(outputName + ".gcode", 'rb')}
#
# r = requests.post(url, headers=headers, files=files)
# r = requests.get
# print r.starus_code

#this is for urlib2
url = "http://" + "octopi.local" + "/api/files/local"
print "URL: " + url

http_header = {
                "User-Agent" : "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36",
                    #switch to user ip var
                #"Host" : "octopi.local",
                #"Origin:" : "http://octopi.local",
                #"Accept" : "application/json, text/javascript, */*; q=0.01",
                #"Referer" : "http://prusa.local/",
                "Accept-Language" : "en-US,en;q=0.8",
                "Accept-Encoding" : "gzip, deflate",
                #"Content-Type": "multipart/form-data; boundary=----WebKitFormBoundaryDeC2E3iWbTv1PwMC",
                #"Content-Type" : "multipart/form-data",
                "Content-Type" : "form-data",
                "X-Api-Key": "156A8AE4000940CFB3C51C9DFD812D8A",
                "X-Requested-With" : "XMLHttpRequest"
                }
data = {
    "Content-Disposition" : "form-data; name='file'; filename='octoupload.gcode'",
    "Content-Type" : "application/octet-stream"
}

files = {
    'file': open(outputName + ".gcode", 'rb'),
    "filename" : "octoupload" + ".gcode"
}

# setup socket connection timeout
timeout = 15
socket.setdefaulttimeout(timeout)

# setup cookie handler
cookie_jar = cookielib.LWPCookieJar()
cookie = urllib2.HTTPCookieProcessor(cookie_jar)

# create an urllib2 opener()
#opener = urllib2.build_opener(proxy, cookie) # with proxy
opener = urllib2.build_opener(cookie) # we are not going to use proxy now

# create your HTTP request
req = urllib2.Request(url, urllib.urlencode(data), http_header, urllib.urlencode(files))

print "Uploading..."

# submit your request
res = opener.open(req)
html = res.read()
response = urllib2.urlopen(req)

print "Response: " + response

# save retrieved HTML to file
open("tmp.html", "w").write(html)
print "HTML" + html

print "done"
