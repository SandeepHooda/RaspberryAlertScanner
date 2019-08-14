#!/bin/bash
a=0

while [ $a -lt 10 ]
do
checkDir1="/home/pi/picamera-motion/cameraLive/cameraActive1"
checkDir2="/home/pi/picamera-motion/cameraLive/cameraActive2"
path="/home/pi/picamera-motion/cameraLive/static"
image_temp="${path}/image_temp.jpg"
image1="${path}/1.jpg"
image2="${path}/2.jpg"

if [ -d "$checkDir1" ]; then
  curl -u admin:ForgetNot85 http://192.168.0.151/tmpfs/auto.jpg?dummy=1565715984878444 --output "$image_temp"
  mv "$image_temp" "$image1"
fi
if [ -d "$checkDir2" ]; then
  curl -u admin:ForgetNot85 http://192.168.0.150/tmpfs/auto.jpg?dummy=1565715984878444 --output "$image_temp"
  mv "$image_temp" "$image2"
fi
sleep 0.5
done
