window.onload = function () {
  if (navigator.geolocation) {
      navigator.geolocation.getCurrentPosition(geolocationSuccess, geolocationFailure);
      console.log('Поиск начался');
  } else {
      console.log('Не найдено');
  }
};


function geolocationSuccess(position) {
	alert("Последний раз вас засекали здесь: " +
	         position.coords.latitude + ", " + position.coords.longitude);
}

function geolocationFailure(positionError) {
    if(positionError == 1) {
		alert("Вы решили не предоставлять данные о своем местоположении, " +
		        "но это не проблема. Мы больше не будем запрашивать их у вас.");
	}
	else if(positionError == 2) {
		alert("Проблемы с сетью или нельзя связаться со службой определения " +
		        "местоположения по каким-либо другим причинам.");
	}
	else if(positionError == 3) {
		alert("He удалось определить местоположение "
		        + "в течение установленного времени. ");

	}
	else {
		alert("Загадочная ошибка.");
	}
}