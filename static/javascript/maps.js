// This file to to pass the javascript call abck function to the google api on the map.html
map_container = document.querySelector('#map_holder')

function get_info() {
    //  Function to grab my custom map from the google maps api
    let geocoder;

    // Coordinates for the United States. This were I want my map to center. Tracking packages across USA
    const USA_Coords = {
        lat: 37.0902,
        lng: -95.7129,
    };

    // initilize geocoder
    geocoder = new google.maps.Geocoder();

    // initilize new map to display that centers United States with a zoom of 4
    const basicMap = new google.maps.Map(map_container, {
        center: USA_Coords,
        zoom: 4,
    });

    // My fetch to grab the data from the location route
    fetch('/location')
        .then((response) => response.json())
        .then((responseData) => {
            locations = responseData['location'];  // Grabs the values of location from my library which returns a list
            // Loops through each location 
            for (let i = 0; i < locations.length; i++) {
                console.log(locations[i])
                geocoder.geocode({ address: String(locations[i]) }, function (results, status) { // Gets the lat and long from the geocode api for each location
                    if (status == 'OK') { // If status is good
                        let marker = new google.maps.Marker({ // place a marker on that location on the center map
                            map: basicMap,
                            position: results[0].geometry.location
                        });
                    }
                    else {
                        alert('Geocode was not successful for the following reason: ' + status); // If not successful, show the error message. 
                    }
                });
            }
        })
};


