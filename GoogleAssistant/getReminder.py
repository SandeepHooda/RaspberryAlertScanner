#!/usr/bin/python3

import requests
import urllib.request
import json 
import os
import subprocess
import os.path



def getReminder():
    myurl = "https://idonotremember-app.appspot.com/GetSnoozedReminders?queryEmail=sonu.hooda@gmail.com"
    req = urllib.request.Request(myurl)
    
    response = urllib.request.urlopen(req)
    return response.read().decode('utf-8')
    
    
def localGoogleAssistPrecessing(text):
    body = {'command':text,'user':'sanhoo'} 

    myurl = "http://192.168.0.120:3000/assistant"
    req = urllib.request.Request(myurl)
    req.add_header('Content-Type', 'application/json; charset=utf-8')
    jsondata = json.dumps(body)
    jsondataasbytes = jsondata.encode('utf-8')   # needs to be bytes
    req.add_header('Content-Length', len(jsondataasbytes))
    print (jsondataasbytes)
    response = urllib.request.urlopen(req, jsondataasbytes)
    return( response.read().decode('utf-8'));

def downLoadWavFile(filePath):
    r = requests.get(filePath, allow_redirects=True)
    open('reminder.wav', 'wb').write(r.content)



remindertext = getReminder();
if remindertext :
    wavFileText = localGoogleAssistPrecessing(remindertext);
    wavFileJson = json.loads(wavFileText);
    print (wavFileJson["audio"])
    downLoadWavFile(wavFileJson["audio"]);

if os.path.exists('reminder.wav'):
    subprocess.run(["aplay", "reminder.wav"])
    os.remove("reminder.wav")

