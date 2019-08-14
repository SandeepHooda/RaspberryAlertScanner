#!/usr/bin/python
import shutil
import os, sys, stat
from flask import Flask, request, render_template, jsonify
app = Flask(__name__)


@app.route('/')
def index():
    return render_template("index.html")

@app.route('/activateCamera/<id>')
def activateCamera(id):
    active="True"
    path= "/home/pi/picamera-motion/cameraLive/cameraActive"+id
    if (os.path.isdir(path)) :
       shutil.rmtree(path, ignore_errors=False, onerror=None)
       active="False"
    else :
       os.mkdir(path)
       os.chmod(path, 0o777)
    return active


if __name__ == '__main__':
    app.run(host='0.0.0.0')
