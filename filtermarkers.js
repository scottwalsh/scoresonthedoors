		function boxclick(box,category) {
		    if (box.checked) {
		      show(category);
		    } else {
		      hide(category);
		    }
      	}
      	   	
      	// A little bit hacky: identify the classification of a marker by checking the first character of the title
      
	   function show(category) {
	   		if (markersArray) {
				for (i in markersArray) {
				
				  if (markersArray[i].title.charAt(0) == category.charAt(0)) {
				    markersArray[i].setMap(map);
				  }
				}
		    }
		}
		
		function hide(category) {
			if (markersArray) {
				for (i in markersArray) {
				  if (markersArray[i].title.charAt(0) == category.charAt(0)) {
				    markersArray[i].setMap(null);
				  }
				}
			}
		}
