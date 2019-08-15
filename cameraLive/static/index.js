let isClientActive = false;
let cam1Active = false;
let cam2Active = false;
let intervalHandel = null

function sendHeartBeat() {
var xhttp = new XMLHttpRequest();
	xhttp.onreadystatechange = function() {
	    if (this.readyState == 4 && this.status == 200) {
               document.getElementById("currentTime").innerHTML = new Date();
	    }
	};
	xhttp.open("GET", "/clientHearBeat", true);
	xhttp.send();
}
function loadCameraImage() {
  if (intervalHandel == null ){
	 intervalHandel = setInterval(function(){ 
         if (!isClientActive) {
	    clearInterval(intervalHandel);
            intervalHandel = null;
	 }else {
            if (cam1Active) {
                document.getElementById("img1").src = "/static/dot.jpg"
		document.getElementById("img1").src = "/static/1.jpg?random="+Math.random();
	    }
	    if (cam2Active ){
                document.getElementById("img2").src = "/static/dot.jpg"
		document.getElementById("img2").src = "/static/2.jpg?random="+Math.random();
            }
	    if (cam1Active || cam2Active) {
               sendHeartBeat();
             }
         }
         
	 
       }, 500);
  }
  
}

function toggleCameraActivity(id) {
     var xhttp = new XMLHttpRequest();
	xhttp.onreadystatechange = function() {
	    if (this.readyState == 4 && this.status == 200) {
               
	       checkIsClientActive();
	    }
	};
	xhttp.open("GET", "/toggleCamera/"+id, true);
	xhttp.send();
}


function isCameraActive(id) {

  var xhttp = new XMLHttpRequest();
	xhttp.onreadystatechange = function() {
	    if (this.readyState == 4 && this.status == 200) {
               var cam1ActiveButtonID = document.getElementById("cam1ActiveButton");
	       var cam2ActiveButtonID = document.getElementById("cam2ActiveButton");
	       if (xhttp.responseText == "True"){
                 if (id == "1"){
                    cam1Active = true;
                    cam1ActiveButtonID.innerHTML = "Turn off cam 1";
                 }else {
		    cam2Active = true;
		    cam2ActiveButtonID.innerHTML = "Turn off cam 2";
                 }
               }else {
		
		if (id == "1"){
		    cam1Active = false;
                    cam1ActiveButtonID.innerHTML = "Turn On cam 1";
                 }else {
		    cam2Active = false;
		    cam2ActiveButtonID.innerHTML = "Turn On cam 2";
                 }
               }

	    }
	};
	xhttp.open("GET", "/isCameraActive/"+id, true);
	xhttp.send();
}
function checkIsClientActive() {
       var xhttp = new XMLHttpRequest();
	xhttp.onreadystatechange = function() {
	    if (this.readyState == 4 && this.status == 200) {
	       if (xhttp.responseText == "True"){
                 isClientActive = true;
	         loadCameraImage();
                  
               }else {
		isClientActive = false;
               }
	       isCameraActive('1');
	       isCameraActive('2');

	    }
	};
	xhttp.open("GET", "/isClientActive", true);
	xhttp.send();
}
