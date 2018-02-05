	start_time_left_hours = 1;
	start_time_left_minutes = 13;
	start_time_left_seconds = 43;

	start_time = new Date();
	
	expires = new Date();
	issued = new Date();

	expires.setHours(start_time.getHours() + start_time_left_hours);
	expires.setMinutes(start_time.getMinutes() + start_time_left_minutes);

	expires_hours = parseInt(expires.getHours())
	if (expires_hours < 10) {
		expires_hours = "0" + expires_hours;
	}
	expires_minutes = parseInt(expires.getMinutes())
	if (expires_minutes < 10) {
		expires_minutes = "0" + expires_minutes;
	}

	var expires_str = expires_hours + ":" + expires_minutes;
	document.getElementById("expires").innerHTML = expires_str;

	issued.setHours(expires.getHours() - 1);
	issued.setMinutes(expires.getMinutes() - 20);

	issued_hours = parseInt(issued.getHours())
	if (issued_hours < 10) {
		issued_hours = "0" + issued_hours;
	}
	issued_minutes = parseInt(issued.getMinutes())
	if (issued_minutes < 10) {
		issued_minutes = "0" + issued_minutes;
	}
	issued_date = parseInt(issued.getDate())
	if (issued_date < 10) {
		issued_date = "0" + issued_date;
	}
	issued_month = parseInt(issued.getMonth() + 1)
	if (issued_month < 10) {
		issued_month = "0" + issued_month;
	}
	issued_year = parseInt(issued.getYear() + 1900)

	var issued_str = issued_date + "/" + issued_month + "/" + issued_year + " " + issued_hours + ":" + issued_minutes;
	document.getElementById("issued").innerHTML = issued_str;


	setInterval(function() {
 
		// find the amount of "seconds" between now and target
		var current_date = new Date().getTime();
		var seconds_left = (expires - current_date) / 1000;
	 
		// do some time calculations
		seconds_left = seconds_left % 86400;
		
		hours = parseInt(seconds_left / 3600);
		if (hours < 10) {
			hours = "0" + hours;
		}
		seconds_left = seconds_left % 3600;
		 
		minutes = parseInt(seconds_left / 60);
		if (minutes < 10) {
			minutes = "0" + minutes;
		}
		seconds = parseInt(seconds_left % 60);
		if (seconds < 10) {
			seconds = "0" + seconds;
		}
		 
		// format countdown string + set tag value
		document.getElementById("timer").innerHTML = hours + ":" + minutes + ":" + seconds;  
 

	}, 1000)
