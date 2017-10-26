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

	var polyline_encoded="sieiHyezLqBKa@iD}@oH_@_CQw@_@GPUBYSkBEQBo@@s@@oAASKo@s@iC[kA[eAs@iCe@cBq@cCm@wDMq@yAwJcFmTuA_G]yB]iAQ[FWk@mAgBcDw@{ACMBm@?e@[}AKs@E]GIMWQYE?MHQgAY\\qCkPMm@IEIKKWAa@DYBG@A}@{BmByE_GuN{DsJ]u@eAkCeDmIaGqNgAoDYk@mAyDeBgFcC_Is@gCm@wCg@eCWyBeAaL_CeVu@{G?g@^{Gj@iJHaBVeC|@iMTcDt@gKR_DN_BNe@CKAM@UBIFo@XuFLcCt@gKt@{Jn@eJReBDaAJy@\\yDz@gJ`Dk]hB_Ob@gDjAoI|AcL\\}BV{BtAcQnA_ODs@La@p@uAf@cA\\wlgiH_plMf@_AHa@Re@v@cBVm@Zu@B_@CMIOa@m@_@i@CK@Wl@gF`AuIj@gFgKpH{AnAe@X`@jB\\sieiHyezLqBKa@iD}@oH_@_CQw@_@GPUBYSkBEQBo@@s@@oAASKo@s@iC[kA[eAs@iCe@cBq@cCm@wDMq@yAwJcFmTuA_G]yB]iAQ[FWk@mAgBcDw@{ACMBm@?e@[}AKs@E]GIMWQYE?MHQgAY\\qCkPMm@IEIKKWAa@DYBG@A}@{BmByE_GuN{DsJ]u@eAkCeDmIaGqNgAoDYk@mAyDeBgFcC_Is@gCm@wCg@eCWyBeAaL_CeVu@{G?g@^{Gj@iJHaBVeC|@iMTcDt@gKR_DN_BNe@CKAM@UBIFo@XuFLcCt@gKt@{Jn@eJReBDaAJy@";
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