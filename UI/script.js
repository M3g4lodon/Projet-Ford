"use script";

/*
$("#connecter").click(function(){
    $.post(--URL de la fonction pour enregistrer un utilisateur--,
    {
        Name: $('#Name').val(),
        FirstName: $('#FirstName').val()
    },
    --call-back function?--
}); 
*/



function TypeUtilisateur() {
	$(".dropdown-menu li a").click(function(){
	  var selText = $(this).text()
	  $(this).parents('.btn-group').find('.dropdown-toggle').html(selText+' <span class="caret"></span>');
	  preferences.type=selText
	  console.log("type set to: "+preferences.type)
	});
}

var preferences={
	type: "Défaut",
	P_Permis: "false",
	P_Meteo: "true",
	P_Charge:"false"
}

$(function() {
		$('#P_Permis').change(function() {
		var state=$(this).prop('checked')
		preferences.P_Permis=state
		console.log("permis set to: "+state)
		})
})
$(function() {
		$('#P_Meteo').change(function() {
		var state=$(this).prop('checked')
		preferences.P_Meteo=state
		console.log("meteo set to: "+state)
		})
})
$(function() {
		$('#P_Charge').change(function() {
		var state=$(this).prop('checked')
		preferences.P_Charge=state
		console.log("charge set to: "+state)
		})
})


var itineraire={
	origine: "",
	destination: ""
}

function GetItineraires(){
	itineraire.origine = $('#origine').val();
	itineraire.destination = $('#destination').val();
	console.log("origine set to: " + itineraire.origine)
	console.log("destination set to: " + itineraire.destination)

	$("#intro_itineraire"
		).html("Basé sur vos préférences, nous avons calculé 3 trajets afin de vous rendre à "+ itineraire.destination)

}


function initMap() {
	var origin = {lat: 48.8566, lng: 2.3522};
	var destination ={lat: 48.8566, lng: 2.3522};
	var map = new google.maps.Map(document.getElementById('map'), {
		zoom: 12,
		center: origin
	});
	console.log(map)

/*
	var marker_origin = new google.maps.Marker({
		position: origin, //to do
		map: map
	});

	console.log(marker_origin)
	var marker_destination = new google.maps.Marker({
		position: destination, //to do
		map: map
	});
*/

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




$(document).ready(TypeUtilisateur)
