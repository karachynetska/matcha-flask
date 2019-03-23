window.onload = function () {
  if (navigator.geolocation) {
      navigator.geolocation.getCurrentPosition(geolocationSuccess, geolocationFailure);
  } else {
      console.log('Your browser does not support geolocation');
  }
};


function geolocationSuccess(position) {
	var data = {
		'latitude': position.coords.latitude,
		'longitude': position.coords.longitude
	};

	$.ajax({
		type: 'POST',
		data: data,
		url: '/ajax_set_geolocation'
	});
}

function geolocationFailure(positionError) {
	$.getJSON('https://json.geoiplookup.io/api?callback=?', function(geo) {

		var data = {
			'latitude': geo.latitude,
			'longitude': geo.longitude
		};

		$.ajax({
			type: 'POST',
			data: data,
			url: '/ajax_set_geolocation'
		});
	});
}
