#!/bin/bash
 heatBeatFile="/home/pi/picamera-motion/cameraLive/static/clientHeartBeat.txt"
  while IFS= read -r line
  do
   now=$(date +'%s')
   diff="$(($now - $line))"
   if [ $line != '' ]; then
      if [ $diff -lt 10 ]; then 
          echo $diff
       else 
         echo "client in active"
      fi
   else
      echo "client in active"
   fi
   sleep 1
  done < "$heatBeatFile"
