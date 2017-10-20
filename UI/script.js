"use script";

function initMap() {
	var paris = {lat: 48.8566, lng: 2.3522};
	var map = new google.maps.Map(document.getElementById('map'), {
		zoom: 12,
		center: paris
	});
	var marker = new google.maps.Marker({
		position: paris,
		map: map
	});
}
