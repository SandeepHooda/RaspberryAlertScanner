#!/bin/bash
a=0
checkDir1="/home/pi/picamera-motion/cameraLive/cameraActive1"
checkDir2="/home/pi/picamera-motion/cameraLive/cameraActive2"
heatBeatFile="/home/pi/picamera-motion/cameraLive/static/clientHeartBeat.txt"
path="/home/pi/picamera-motion/cameraLive/static"
image_temp="${path}/image_temp.jpg"
image1="${path}/1.jpg"
image2="${path}/2.jpg"


while [ $a -lt 10 ]
do

#If heart beat is too old then delete marker directory to indicate to turn offf camera feed.

while IFS= read -r line
  do
   now=$(date +'%s')
   diff="$(($now - $line))"
   if [ $line != '' ]; then
      if [ $diff -lt 10 ]; then
          echo $diff
       else
         echo "deleteing file"
         if [ -d "$checkDir1" ]; then
           rmdir $checkDir1
         fi
         if [ -d "$checkDir2" ]; then
           rmdir $checkDir2 
         fi
      fi
   else
      #echo "client in active"
       rmdir $checkDir1
       rmdir $checkDir2
   fi
  done < "$heatBeatFile"

clientActive="False"
if [ -d "$checkDir1" ]; then
  curl -u admin:ForgetNot85 http://192.168.0.151/tmpfs/auto.jpg?dummy=1565715984878444 --output "$image_temp"
  mv "$image_temp" "$image1"
  clientActive="True"
fi
if [ -d "$checkDir2" ]; then
  curl -u admin:ForgetNot85 http://192.168.0.150/tmpfs/auto.jpg?dummy=1565715984878444 --output "$image_temp"
  mv "$image_temp" "$image2"
  clientActive="True"
fi

if [ clientActive = "True" ] 
then
  sleep 0.2
else
  sleep 2
fi
done
