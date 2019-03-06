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
	console.log(data);

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
			url: '/ajax_set_location'
		});
	});
    // if(positionError == 1) {
	// 	alert("Вы решили не предоставлять данные о своем местоположении, " +
	// 	        "но это не проблема. Мы больше не будем запрашивать их у вас.");
	// }
	// else if(positionError == 2) {
	// 	alert("Проблемы с сетью или нельзя связаться со службой определения " +
	// 	        "местоположения по каким-либо другим причинам.");
	// }
	// else if(positionError == 3) {
	// 	alert("He удалось определить местоположение "
	// 	        + "в течение установленного времени. ");
	//
	// }
	// else {
	// 	alert("Загадочная ошибка.");
	// }
}
