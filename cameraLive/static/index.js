function loadCameraImage() {
  setInterval(function(){ 
      document.getElementById("img1").src = "/static/1.jpg?random="+Math.random();
      document.getElementById("img2").src = "/static/2.jpg?random="+Math.random();
    }, 1000);
}
