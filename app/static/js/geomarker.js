var marker;

function initEditMap() {
  var map = new google.maps.Map(document.getElementById('map_edit'), {
    zoom: 13,
    center: {lat: 59.325, lng: 18.070}
  });

  marker = new google.maps.Marker({
    map: map,
    draggable: true,
    animation: google.maps.Animation.DROP,
    position: {lat: 59.327, lng: 18.067}
  });
  marker.addListener('click', toggleBounce);
}

function toggleBounce() {
  if (marker.getAnimation() !== null) {
    marker.setAnimation(null);
  } else {
    marker.setAnimation(google.maps.Animation.BOUNCE);
  }
}



// function initEditMap() {
//   var myLatLng = {lat: -25.363, lng: 131.044};
//
//   var map = new google.maps.Map(document.getElementById('map_edit'), {
//     zoom: 4,
//     center: myLatLng
//   });
//
//   var marker = new google.maps.Marker({
//     position: myLatLng,
//     map: map,
//     title: 'Hello World!'
//   });
// }

// var myLatlng = new google.maps.LatLng(-25.363882,131.044922);
// var mapOptions = {
//   zoom: 4,
//   center: myLatlng
// }
// var map = new google.maps.Map(document.getElementById("map_edit"), mapOptions);
//
// var marker = new google.maps.Marker({
//     position: myLatlng,
//     title:"Hello World!"
// });
//
// // To add the marker to the map, call setMap();
// marker.setMap(map);