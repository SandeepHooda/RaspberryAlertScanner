#!/usr/bin/python
import time
import smtplib, ssl
import os
import glob
import shutil
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import subprocess
import os, sys, stat
import requests
import urllib.request
import base64
import traceback

username = 'foscamnotificationsandeep@gmail.com'
password = '' #//This password is in post master, raspberry pi, D3D cameras


port = 587  # For starttls
smtp_server = "smtp.gmail.com"
sender_email = username
receiver_email = "sonu.hooda@gmail.com"
password = password
message = """\
Subject: Camera D

Your camera is not working id : """



class CameraStatus(object):
    def __init__(self, id, status, ftpID, ipAddress):
        self.id = id
        self.status = status
        self.ftpID = ftpID;
        self.ipAddress = ipAddress;
allCameraStatus = []

allCameraStatus.append(CameraStatus("5", False, "1", "192.168.0.151"))
allCameraStatus.append(CameraStatus("8", False, "2", "192.168.0.150"))

for obj in allCameraStatus:
    print (obj.id, obj.status)
    
def sendEmail(subject, body) :
    context = ssl.create_default_context()
    with smtplib.SMTP(smtp_server, port) as server:
        server.ehlo()  # Can be omitted
        server.starttls(context=context)
        server.ehlo()  # Can be omitted
        server.login(sender_email, password)
        msg = MIMEMultipart()
        msg['Subject'] = subject
        body = body
        msg.attach(MIMEText(body, 'plain'))
        server.sendmail(sender_email, receiver_email, msg.as_string())

def captureImage(path, ip) :
  files = [f for f in glob.glob(path + "**/*.jpg", recursive=True)]
  if (len(files) > 0):
     print(" there are images already ")
     return #Already has images no need to check further with camera
  else:
     print(" I wil capture image from camera")
  try:
     out_file_path=path+ip+"_imageCapture.jpg"
     download_url="http://"+ip+"/tmpfs/auto.jpg?dummy="+str(time.time())
     req = urllib.request.Request(download_url)
     username="admin"
     password="ForgetNot85"
     credentials = ('%s:%s' % (username, password))
     encoded_credentials = base64.b64encode(credentials.encode('ascii'))
     req.add_header('Authorization', 'Basic %s' % encoded_credentials.decode("ascii"))
  
     with urllib.request.urlopen(req) as response, open(out_file_path, 'wb') as out_file:
       data = response.read()
       out_file.write(data)
     #print("check you image now:"+out_file_path) 
     os.chmod( out_file_path, 0o777)
     #time.sleep(60)  
  except:
     #traceback.print_exc();
     print("could not connect to "+ip)

def checkFtpLocation(path) :
    
    files = [f for f in glob.glob(path + "**/*.jpg", recursive=True)]
    if (len(files) > 0):
        shutil.rmtree(path, ignore_errors=False, onerror=None)
        os.mkdir(path)
        os.chmod(path, 0o777)
        return True
    else:
        return False

while(True):
    try:
        for obj in allCameraStatus:
            print("Monitor on for "+obj.id)
            path = "/home/pi/ftp/d3d_"+obj.ftpID+"/";
            captureImage(path, obj.ipAddress)
            cameraStatus = checkFtpLocation(path)
            if (cameraStatus != obj.status):
                if (cameraStatus):
                    sendEmail("camera is up","camera "+obj.ftpID);
                else:
                    sendEmail("camera is down","camera "+obj.ftpID);
                    
                obj.status = cameraStatus
            # Send heart beat every 60 second FTP sends photo every 18 seconds
            url = "http://sanhoo-home-security.appspot.com/IamAlive?id="+obj.id+"&alarmTriggered="
            if (cameraStatus):
                requests.get(url+"N")
            else:
                requests.get(url+"Y")
        time.sleep(60)
    except:
        print("Error in monitor")
        
    
