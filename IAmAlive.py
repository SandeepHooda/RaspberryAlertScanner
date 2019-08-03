#!/usr/bin/python
import time
import requests


while(True):
    try:
        requests.get("http://sanhoo-home-security.appspot.com/IamAlive?id=6")
    except:
        print("Error in reporting health")
    
    time.sleep(10)