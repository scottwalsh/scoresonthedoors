		var map;
		var markersArray = [];
	 
		function load() {
		  map = new google.maps.Map(document.getElementById("map"), {
		    center: new google.maps.LatLng(53.742676,-0.337574), // St Stephen's (the center of the universe)
		    zoom: 11,
		    mapTypeId: 'roadmap'
		  });
		  var infoWindow = new google.maps.InfoWindow;
	 
		  // Change this depending on the name of your PHP file
		  downloadUrl("markers.xml", function(data) {
		    var xml = data.responseXML;
		    var markers = xml.documentElement.getElementsByTagName("marker");
		    for (var i = 0; i < markers.length; i++) {
		      var name = markers[i].getAttribute("name");
		      var address = markers[i].getAttribute("address");
		      var postcode = markers[i].getAttribute("postcode");        
		      var point = new google.maps.LatLng(
		          parseFloat(markers[i].getAttribute("lat")),
		          parseFloat(markers[i].getAttribute("lng")));
		      var accuracy = markers[i].getAttribute("accuracy");
		      var inspection = markers[i].getAttribute("inspection");
		      var score = markers[i].getAttribute("score");
		      var classification = markers[i].getAttribute("classification");
		      var telephone = markers[i].getAttribute("telephone");
		      var type = markers[i].getAttribute("type");
		      var html = "<b>" + name + "<\/b> <br>" + address + "<br>" + score + "<br>" + classification;
		      var iconImage = setIconImage(score);
		      var marker = new google.maps.Marker({
		        map: map,
		        position: point,
		        icon: iconImage,
		        title: classification + " - " + name,
		        shadow: 'http://labs.google.com/ridefinder/images/mm_20_shadow.png'
		      });
		      markersArray.push(marker);
		      bindInfoWindow(marker, map, infoWindow, html);
		    }
		  });
		}
	 
		function bindInfoWindow(marker, map, infoWindow, html) {
		  google.maps.event.addListener(marker, 'click', function() {
		    infoWindow.setContent(html);
		    infoWindow.open(map, marker);
		  });
		}
	 
		function downloadUrl(url, callback) {
		  var request = window.ActiveXObject ?
		      new ActiveXObject('Microsoft.XMLHTTP') :
		      new XMLHttpRequest;
	 
		  request.onreadystatechange = function() {
		    if (request.readyState == 4) {
		      request.onreadystatechange = doNothing;
		      callback(request, request.status);
		    }
		  };
	 
		  request.open('GET', url, true);
		  request.send(null);
		}
	 
		function doNothing() {}
		
		function setIconImage(score)
		{
		    if (score < 60) {
		      return 'http://labs.google.com/ridefinder/images/mm_20_red.png';
		    }
		    if (score < 75) {
		      return 'http://labs.google.com/ridefinder/images/mm_20_orange.png';
		    }
		    if (score < 90) {
		      return 'http://labs.google.com/ridefinder/images/mm_20_yellow.png';
		    }
		    if (score <= 100) {
		      return 'http://labs.google.com/ridefinder/images/mm_20_green.png';
		    }
			return 'http://labs.google.com/ridefinder/images/mm_20_gray.png';
		}
