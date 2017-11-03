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
const ROOT = window.location.href


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


function GetItineraires(){
	$.ajax({
        url: ROOT + 'itineraire',
        data: {
            TypeUser: preferences.type,
            P_Permis: preferences.P_Permis,
            P_Meteo: preferences.P_Meteo,
            P_Charge: preferences.P_Charge,
            origine: $('#origine').val(),
            destination: $('#destination').val()
        },
        success: function (data) {
            console.log(data);
            $("#intro_itineraire"
            ).html("Basé sur vos préférences, nous avons calculé 3 trajets afin de vous rendre à ")
        	},
        dataType: "json"
    	})}


$(document).ready(TypeUtilisateur)
$(window).load(GetItineraires)

// Variables de test
var suggested_itineraries={
	origin:{
		address:"chatelet les halles",
		lat:48.8619,
		lng:2.3470
	},
	destination :{
		address:"gare de lyon, paris",
		lat:48.8443,
		lng:2.3744
	},

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


var map;

// Création de la carte par défaut
function initMap() {
	var center ={lat: 48.8566, lng: 2.3522};
	map = new google.maps.Map(document.getElementById('map'), {
		zoom: 12,
		center: center
	});
}

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


	var marker_origin = new google.maps.Marker({
		position: {lat:suggested_itineraries.origin.lat, lng:suggested_itineraries.origin.lng},
		map: map,
	});

	var marker_destination = new google.maps.Marker({
		position: {lat:suggested_itineraries.destination.lat, lng:suggested_itineraries.destination.lng},
		map: map
	});

}
