var inner_shire;
var outer_shire;


jQuery(document).ready(function () {
    var map;

    var style = [
		{
		stylers: [
			{ saturation: "-100" },
			{ lightness: "20" }
		]
		},{
		featureType: "poi",
		stylers: [
			{ visibility: "off" }
		]
		},{
		featureType: "transit",
		stylers: [
			{ visibility: "off" }
		]
		},{
		featureType: "road",
		stylers: [
			{ lightness: "50" },
			{ visibility: "on" }
		]
		},{
		featureType: "landscape",
		stylers: [
			{ lightness: "50" }
		]
		}
	]
    
    var pt_office = new google.maps.LatLng(37.4426011,-122.1643497)

    var options = {
        zoom: 13,
        center:  pt_office,
        mapTypeId: google.maps.MapTypeId.ROADMAP,
        disableDefaultUI: true
    };
    
    var map = new google.maps.Map($('#map')[0], options);
    map.setOptions({
        styles: style
    });
    
    var marker = new google.maps.Marker({
                        position: pt_office,
                        map: map,
                        clickable: false,
                    });
    var inner_shire = new google.maps.MVCArray([]);
    var outer_shire = new google.maps.MVCArray([]);
    
    var is_heatmap = new google.maps.visualization.HeatmapLayer({
        data : inner_shire,
        opacity: .3,
        map : map,
    });
    
    var os_heatmap = new google.maps.visualization.HeatmapLayer({
        data : outer_shire,
        gradient: [
            'rgba(0, 255, 255, 0)',
            'rgba(0, 255, 255, 1)',
            'rgba(0, 191, 255, 1)',
            'rgba(0, 127, 255, 1)',
            'rgba(0, 63, 255, 1)',
            'rgba(0, 0, 255, 1)',
            'rgba(0, 0, 223, 1)',
            'rgba(0, 0, 191, 1)',
            'rgba(0, 0, 159, 1)',
            'rgba(0, 0, 127, 1)',
            'rgba(63, 0, 91, 1)',
            'rgba(127, 0, 63, 1)',
            'rgba(191, 0, 31, 1)',
            'rgba(255, 0, 0, 1)',
        ],
        opacity: .3,
        map : map,
    });
    
    var shires;
    $.getJSON("shires.json", function( data ) {
        console.log(data)
        data["inner_shire"].forEach(function(pt) {
           inner_shire.push(new google.maps.LatLng(pt[0], pt[1]));
        });
        data["outer_shire"].forEach(function(pt) {
           outer_shire.push(new google.maps.LatLng(pt[0], pt[1]));
        });
    });

});


