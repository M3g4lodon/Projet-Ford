"use script";

function initMap() {
	var origin = {lat: 48.8566, lng: 2.3522};
	var destination ={lat: 48.8566, lng: 2.3522};
	var map = new google.maps.Map(document.getElementById('map'), {
		zoom: 12,
		center: origin
	});
	console.log(map)

	var marker_origin = new google.maps.Marker({
		position: origin, //to do
		map: map
	});

	console.log(marker_origin)
	var marker_destination = new google.maps.Marker({
		position: destination, //to do
		map: map
	});

	var polyline_encoded="yhhiHyefM\\Nb@q@jBeE|@_@Ig@v@gABb@pBe@fHaCrOiFrIuClBo@`@_@HIf@qAt@_Ct@iElBqKP_@VY\\Qr@OnAA|CHrCJr@CVINKR]Tw@PwAd@_FD@Sg@LBNcAfB{It@iECC";
	var polyline_decoded=google.maps.geometry.encoding.decodePath(polyline_encoded);
	var itinerary= new google.maps.Polyline({
		path:polyline_decoded,
		geodesic :true,
		strokeColor :'#FF0000',
		strokeOpacity :1.0,
		strokeWeight :2
	});
	itinerary.setMap(map)
}


function f() {
	$(".dropdown-menu li a").click(function(){
	  var selText = $(this).text();
	  console.log(selText)
	  $(this).parents('.btn-group').find('.dropdown-toggle').html(selText+' <span class="caret"></span>');
	});
}

$(document).ready(f);
