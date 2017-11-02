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

// Convertit une chaine de caractères d'une adresse en coordonnées (lat & lng) dans un format que Google Maps comprend
function ConvertAddressLatLng(address){

    function ExtractAddress(data){
        var lat, lng;
        lat = data.results[0].geometry.location.lat;
        lng = data.results[0].geometry.location.lng;
        return {lat:lat, lng:lng};
    }

    function Error(){
        console.log("Couldn't convert address in lat/lng coord")
    }

    $.ajax({
        url:"https://maps.googleapis.com/maps/api/geocode/json",
        data : {address :address,key:"AIzaSyDpVNzFcwgFfPJOK25P9NlMBL-YEe8bSow"},
        dataType :"json",
        type:"GET",
        success : ExtractAddress,
        error: Error
    });


}

// Fonction appelée lors de la recherche
function GetItineraires(){
	itineraire.origine = $('#origine').val();
	itineraire.destination = $('#destination').val();
	console.log("origine set to: " + itineraire.origine)
	console.log("destination set to: " + itineraire.destination)

	$("#intro_itineraire"
		).html("Basé sur vos préférences, nous avons calculé 3 trajets afin de vous rendre à "+ itineraire.destination)
    var suggested_itineraries = SuggestedItineraries(itineraire, preferences)
    PrintItinerariesOnMap(suggested_itineraries)
}

// Demande les 3 itinéraires suggérés par nos services
function suggested_itineraries(itineraire, preferences){
    console.log("Itinerary search")
}

var map;

// Création de la carte par défaut
function initMap() {
	var center ={lat: 48.8566, lng: 2.3522};
	map = new google.maps.Map(document.getElementById('map'), {
		zoom: 12,
		center: center
	});
}

// Variables de tests
var suggested_itineraries={
	origin:"chatelet les halles",
	destination :"gare de lyon, paris",
	results:[
		{
			polyline_encoded:"yhhiHyefM\\Nb@q@jBeE|@_@Ig@v@gABb@pBe@fHaCrOiFrIuClBo@`@_@HIf@qAt@_Ct@iElBqKP_@VY\\Qr@OnAA|CHrCJr@CVINKR]Tw@PwAd@_FD@Sg@LBNcAfB{It@iECC"
		},
		{
			polyline_encoded:"yhhiHyefM\\Nb@q@jBeE|@_@Ig@v@gABb@pBe@fHaCrOiFrIuClBo@`@_@HIf@qAt@_Ct@iElBqKP_@VY\\Qr@OnAA|CHrCJr@CVINKR]Tw@PwAd@_FD@Sg@LBNcAfB{It@iECC"
		},
		{
			polyline_encoded:"yhhiHyefM\\Nb@q@jBeE|@_@Ig@v@gABb@pBe@fHaCrOiFrIuClBo@`@_@HIf@qAt@_Ct@iElBqKP_@VY\\Qr@OnAA|CHrCJr@CVINKR]Tw@PwAd@_FD@Sg@LBNcAfB{It@iECC"
		}]
};

// Affiche les 3 itinéraires sur la carte, ainsi que le départ et l'arrivée
function PrintItinerariesOnMap(suggested_itineraries){
    var polyline_encoded_1 = suggested_itineraries.results[0].polyline_encoded
	var polyline_decoded_1=google.maps.geometry.encoding.decodePath(polyline_encoded_1);
	var itinerary_1= new google.maps.Polyline({
		path:polyline_decoded_1,
		geodesic :true,
		strokeColor :'#283EA4',
		strokeOpacity :1.0,
		strokeWeight :2.5,
		map:map
	});

    var polyline_encoded_2 = suggested_itineraries.results[1].polyline_encoded
	var polyline_decoded_2=google.maps.geometry.encoding.decodePath(polyline_encoded_2);
	var itinerary_2= new google.maps.Polyline({
		path:polyline_decoded_2,
		geodesic :true,
		strokeColor :'#286090',
		strokeOpacity :1.0,
		strokeWeight :2,
		map:map
	});

    var polyline_encoded_3 = suggested_itineraries.results[2].polyline_encoded
	var polyline_decoded_3=google.maps.geometry.encoding.decodePath(polyline_encoded_3);
	var itinerary_3= new google.maps.Polyline({
		path:polyline_decoded_3,
		geodesic :true,
		strokeColor :'#286090',
		strokeOpacity :1.0,
		strokeWeight :2,
		map:map
	});

	var marker_destination = new google.maps.Marker({
		position: ConvertAddressLatLng(suggested_itineraries.destination),
		map: map
	});
	
	var marker_origin = new google.maps.Marker({
		position: ConvertAddressLatLng(suggested_itineraries.origin),
		map: map
	});

}


$(document).ready(TypeUtilisateur)
