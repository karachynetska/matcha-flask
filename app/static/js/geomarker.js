var marker;

function initEditMap() {
  var latitude = parseFloat($('#geo_edit_latitude').text()),
      longitude = parseFloat($('#geo_edit_longitude').text());

  var map = new google.maps.Map(document.getElementById('map_edit'), {
    zoom: 13,
    center: {lat: latitude, lng: longitude}
  });

  marker = new google.maps.Marker({
    map: map,
    draggable: true,
    animation: google.maps.Animation.DROP,
    position: {lat: latitude, lng: longitude}
  });

  marker.addListener('dragend', function (e) {
    var latitude = e.latLng.lat(),
        longitude = e.latLng.lng();

    $('#change_geolocation').on('click', function (e) {
      e.preventDefault();
      $('#geo_edit_latitude').text(latitude);
      $('#geo_edit_longitude').text(longitude);

      var data = {
        'latitude': latitude,
        'longitude': longitude
      };

      $.ajax({
        type: 'POST',
        data: data,
        url: '/ajax_change_geolocation'
      }).done(function (data) {
        var res = JSON.parse(data);
        if (res.ok == false) {
          $('#change_geo_message').text(res.error);
          $('#change_geo_message').addClass('error_text');
        } else {
          $('#change_geo_message').text(res.error);
          $('#change_geo_message').addClass('success');
        }
      });
    });
  });
}

function initMap() {
    var latitude = parseFloat($('#geo_latitude').text()),
        longitude = parseFloat($('#geo_longitude').text());
	if (!latitude && !longitude) {
		latitude = 50.4688257;
		longitude = 30.4621588;
	}
	var uluru = {lat: latitude, lng: longitude};
	var map = new google.maps.Map(document.getElementById('map'), {
	    zoom: 17,
        center: uluru,
        zoomControl: true,
        scaleControl: false,
        scrollwheel: false,
        disableDoubleClickZoom: true
	});
	var marker = new google.maps.Marker({
        position: uluru,
        map: map
	});
}