#!/usr/bin/python
import shutil
import os, sys, stat
import time
import subprocess
from flask import Flask, request, render_template, jsonify
app = Flask(__name__)


@app.route('/')
@app.route('/index')
def index():
    return render_template("index.html")

@app.route('/toggleCamera/<id>')
def toggleCamera(id):
    active="True"
    path= "/home/pi/picamera-motion/cameraLive/cameraActive"+id
    if (os.path.isdir(path)) :
       shutil.rmtree(path, ignore_errors=False, onerror=None)
       active="False"
    else :
       os.mkdir(path)
       os.chmod(path, 0o777)
    return active

@app.route('/togglePiHumanDetect')
def togglePiHumanDetect():
    active="True"
    path= "/home/pi/picamera-motion/cameraLive/PiHumanDetect"
    if (os.path.isdir(path)) :
       shutil.rmtree(path, ignore_errors=False, onerror=None)
       active="False"
    else :
       os.mkdir(path)
       os.chmod(path, 0o777)
    return active

@app.route('/isOnPiHumanDetect')
def isOnPiHumanDetect():
    active="False"
    path= "/home/pi/picamera-motion/cameraLive/PiHumanDetect"
    if (os.path.isdir(path)) :
       active="True"
    return active


@app.route('/isClientActive')
def isClientActive():
    path1= "/home/pi/picamera-motion/cameraLive/cameraActive1"
    path2= "/home/pi/picamera-motion/cameraLive/cameraActive2"
    if (os.path.isdir(path1) or os.path.isdir(path2)  ) :
       return "True"
    else :
       return "False"

@app.route('/isCameraActive/<id>')
def isCameraActive(id):
    path= "/home/pi/picamera-motion/cameraLive/cameraActive"+id
    if (os.path.isdir(path) ) :
       return "True"
    else :
       return "False"

@app.route('/shutdown')
@app.route('/reboot')
def shutdownHtml():
    return render_template("reboot.html");


@app.route('/shutdownPi')
def shutdownPi():
    subprocess.run(["aplay", "/home/pi/music/shutdown.wav"]);
    subprocess.run(["sudo", "shutdown","-h","now"]);


@app.route('/rebootPi')
def rebootPi():
    subprocess.run(["aplay", "/home/pi/music/reboot.wav"]);
    subprocess.run(["sudo", "reboot","now"]);   

@app.route('/clientHearBeat')
def clientHearBeat():
    f= open("/home/pi/picamera-motion/cameraLive/static/clientHeartBeat.txt","w+")
    timeinSeconds= str(int(time.time()));
    f.write(timeinSeconds)
    f.write("\n")
    f.close() 
    return timeinSeconds


if __name__ == '__main__':
    app.run(host='0.0.0.0')
