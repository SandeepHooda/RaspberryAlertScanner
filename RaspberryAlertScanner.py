import urllib.request
import time
import numpy as np
import requests
import base64
from datetime import datetime


if (int(datetime.now().strftime("%Y%m%d%H%M%S")) - imgDate  <60000 ):
	print("Too yong")
else :
	print("Too Old")

while(True):
	time.sleep(1)
	try :	
		allImages = requests.get("http://192.168.0.120:5000/images")
		print(allImages.status_code)
		if ( allImages.status_code == 200) :
			imageArrayByPi = allImages.json()
			for imageName in imageArrayByPi["files"]:
				#imageName = '20190723071808.jpg'
				imgDate = int(imageName[0:14])
				print(imageName)
				imgResp=urllib.request.urlopen('http://192.168.0.120:5000/image/'+imageName)
				data = imgResp.read();
				io_buf = bytearray(data)
				imgNp = np.array(io_buf,dtype=np.uint8)
				
				response = requests.post("http://localhost:80/v1/vision/detection",files={"image":imgNp}).json()
				print(response)
				try :
					imageHasHuman = False;
					if response["success"] :
						if response["predictions"] :
							for object in response["predictions"]:
								print(object["label"])
								label = object["label"]
								if (label == 'person') :
									imageHasHuman = True;
						
					if (imageHasHuman ) :
						if (int(datetime.now().strftime("%Y%m%d%H%M%S")) - imgDate  <180000 ):
							print("Too yong. Make a call and send email")
							encoded_string = base64.b64encode(data)		
							data = {'imageBase64Str':encoded_string}	
							response = requests.post("http://sanhoo-home-security.appspot.com/HumanDetected",data=data)
						else :
							print("Too Old")
						
						requests.get("http://192.168.0.120:5000/moveimage/"+imageName+"/human") # Move to human folder in SD card
					else :
						#requests.get("http://192.168.0.120:5000/moveimage/"+imageName+"/no-human")
						requests.get("http://192.168.0.120:5000/deleteimage/"+imageName) #Delete this 
					
					
				except KeyError:
					print("Invalid response KeyError")
				except:
					print("Something else went wrong")
		else: 
			print("Looks like raspberry py is down")
			time.sleep(10)
	except:
		print("Not able to connect to raspberry pi")
		time.sleep(10)