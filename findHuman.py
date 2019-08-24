#!/usr/bin/python3

import requests
import base64
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import time 
from imageai.Detection import ObjectDetection
import os
import traceback
import glob
import shutil

password = "nqyhmpfsmuiiyyof"

fromaddr = "foscamnotificationsandeep@gmail.com"
toaddr = "sonu.hooda@gmail.com"

ftpPath="/home/pi/ftp/"
shutil.rmtree(ftpPath, ignore_errors=False, onerror=None) # so that the directories with old name (empty dir) gets delete in morning
os.mkdir(ftpPath)
os.chmod(ftpPath, 0o777)

def checkFtpLocation(path) :

    files = [f for f in glob.glob(path + "**/*.jpg", recursive=True)]
    if (len(files) > 0):
      return files
    else :
      return None
def sendEmail(filePath):
  # instance of MIMEMultipart
  msg = MIMEMultipart()

  # storing the senders email address
  msg['From'] = fromaddr

  # storing the receivers email address
  msg['To'] = toaddr

  # storing the subject
  msg['Subject'] = "Human detected by pi"

  # string to store the body of the mail
  body = "Raspberry python script detected human"

  # attach the body with the msg instance
  msg.attach(MIMEText(body, 'plain'))

  # open the file to be sent

  attachment = open(filePath, "rb")

  # instance of MIMEBase and named as p
  p = MIMEBase('application', 'octet-stream')

  # To change the payload into encoded form
  p.set_payload((attachment).read())
  # encode into base64
  encoders.encode_base64(p)
  filename = "Image.jpg"
  p.add_header('Content-Disposition', "attachment; filename= %s" % filename)

  # attach the instance 'p' to instance 'msg'
  msg.attach(p)

  # creates SMTP session
  s = smtplib.SMTP('smtp.gmail.com', 587)

  # start TLS for security
  s.starttls()

  # Authentication
  s.login(fromaddr, password)

  # Converts the Multipart msg into a string
  text = msg.as_string()

  # sending the mail
  s.sendmail(fromaddr, toaddr, text)

  # terminating the session
  s.quit()

#Send Email

def moveFileForFtpMonitor(filePath) :
 oldPath = filePath
 filePath=filePath.replace("ftp", "ftp_monitor") 
 if not os.path.exists(os.path.dirname(filePath)):
    try:
        os.makedirs(os.path.dirname(filePath))
    except OSError as exc: # Guard against race condition
        if exc.errno != errno.EEXIST:
            raise

 #print ("moving file "+oldPath +" to " +filePath)
 os.rename(oldPath, filePath)
#moveFileForFtpMonitor
execution_path = os.getcwd()
#print ("load model from "+execution_path)
detector = ObjectDetection()
detector.setModelTypeAsRetinaNet()
detector.setModelPath( os.path.join(execution_path , "resnet50_coco_best_v2.0.1.h5"))
detector.loadModel(detection_speed="faster")
#detector.loadModel()

while True:

 try:
  
  humanDetectSwitch = False;
  Switch_on= "/home/pi/picamera-motion/cameraLive/PiHumanDetect"
  if (os.path.isdir(Switch_on)) : #else don't run the detect code
    humanDetectSwitch = True;
  
  files = checkFtpLocation(ftpPath)
  if files is not None :
    humanFound = False;
    for imagePath in files :
      if (humanDetectSwitch) :
          if ( not humanFound ) : #If human already found then skip more detection in images of this batch
            print ("check for human presence ")
            detections = detector.detectObjectsFromImage(input_image=os.path.join(execution_path ,imagePath), output_image_path=os.path.join(execution_path , "newd3d.jpg"))
            for eachObject in detections:
              if (eachObject["name"] == "person") :
                print ("Human Found")
                humanFound = True;
                requests.get("http://sanhoo-home-security.appspot.com/IamAlive?id=9&alarmTriggered=Y")
                sendEmail(imagePath)
      
          
      moveFileForFtpMonitor(imagePath)
  #Processing of all files done take some rest
  print ("taking rest now") 
  if (humanDetectSwitch) :
      time.sleep(2)
  else :
      time.sleep(10)
  

  requests.get("http://sanhoo-home-security.appspot.com/IamAlive?id=9")
 except:
  traceback.print_exc()

