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

camera_1_status = False;
camera_2_status = False;
camera_3_status = False;

def sendEmail(subject, body) :
    context = ssl.create_default_context()
    with smtplib.SMTP(smtp_server, port) as server:
        server.ehlo()  # Can be omitted
        server.starttls(context=context)
        server.ehlo()  # Can be omitted
        server.login(sender_email, password)
        msg = MIMEMultipart()
        msg['Subject'] = subject
        body = "Python test mail"
        msg.attach(MIMEText(body, 'plain'))
        server.sendmail(sender_email, receiver_email, msg.as_string())

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
    cameraStatus = checkFtpLocation("/home/pi/ftp/d3d_1/")
    if (cameraStatus != camera_1_status):
        if (cameraStatus):
            sendEmail("camera is up","camera 1");
        else:
            sendEmail("camera is down","camera 1");
            requests.get("http://sanhoo-home-security.appspot.com/HumanDetected?deviceID=5")
    camera_1_status = cameraStatus
    
    time.sleep(60)