var map = L.map('map').setView(
    [19.381074826513803, -99.13842300487916], 12
    );

// set map's minimum zoom
map.setMinZoom(10);
// lock map boundries
map.setMaxBounds([
    [19.660760188533505, -99.41937189586469],
    [19.058925309976264, -98.88988377708824]
]);

L.tileLayer('https://tile.openstreetmap.org/{z}/{x}/{y}.png', {
    maxZoom: 20,
    attribution: '&copy; <a href="http://www.openstreetmap.org/copyright">OpenStreetMap</a>'
}).addTo(map);

var marker = L.marker([19.381074826513803, -99.13842300487916]).addTo(map);

var cfg = {
  "radius": 0.005,
  "maxOpacity": .5,
  "scaleRadius": true,
  "useLocalExtrema": true,
  latField: 'latitud',
  lngField: 'longitud',
}

var apply = document.getElementById('apply');
var asHeatmap = document.getElementById('asHeatmap');
var filtersInput = document.getElementById('filters');
var asCluster = document.getElementById('asCluster');

apply.addEventListener('click', function() {
    //get the values from input field
    filters = filtersInput.value;
    //if filters is not empty
    if (filters) {
        //remove all markers
        map.eachLayer(function(layer) {
            if (layer instanceof L.Marker || layer instanceof HeatmapOverlay || layer instanceof L.MarkerCluster) {
                map.removeLayer(layer);
            }
        })
        //call api endpoint to get coordinates
        fetch('api/getCoordinatesByFilter/?' + filters)
            .then(response => response.json())
            .then(data => {
                // add data as markers to the map
                for (var i = 0; i < data.length; i++) {
                    L.marker([data[i].latitud, data[i].longitud]).addTo(map);
                }
            })
            .catch(error => {
                // handle any errors that occur during the fetch request
                console.error(error);
            });
    }

})

asHeatmap.addEventListener('click', function() {
    //get the values from input field
    filters = filtersInput.value;
    //if filters is not empty
    if (filters) {
        //remove all markers
        map.eachLayer(function(layer) {
            if (layer instanceof L.Marker || layer instanceof HeatmapOverlay || layer instanceof L.MarkerCluster) {
                map.removeLayer(layer);
            }
        })
        //call api endpoint to get coordinates
        fetch('api/getCoordinatesByFilter/?' + filters)
            .then(response => response.json())
            .then(data => {
                var heatmapData = {
                    max: data.length,
                    min: data.length/10,
                    data: data
                };
                cfg.radius= Math.min(5/data.length, 0.006);
                var heatmapLayer = new HeatmapOverlay(cfg);
                heatmapLayer.setData(heatmapData);
                heatmapLayer.addTo(map);
            })
            .catch(error => {
                // handle any errors that occur during the fetch request
                console.error(error);
            });
    }
})

asCluster.addEventListener('click', function() {
    //get the values from input field
    filters = filtersInput.value;
    //if filters is not empty
    if (filters) {
        //remove all markers
        map.eachLayer(function(layer) {
            if (layer instanceof L.Marker || layer instanceof HeatmapOverlay || layer instanceof L.MarkerCluster) {
                map.removeLayer(layer);
            }
        })
        //call api endpoint to get coordinates
        fetch('api/getCoordinatesByFilter/?' + filters)
            .then(response => response.json())
            .then(data => {
                var markers = L.markerClusterGroup();
                for (var i = 0; i < data.length; i++) {
                    var mark = L.marker([data[i].latitud, data[i].longitud]);
                    markers.addLayer(mark);
                }
                markers.addTo(map);
            })
            .catch(error => {
                // handle any errors that occur during the fetch request
                console.error(error);
            });
    }
})

// //call api endpoint to get coordinates
// fetch('api/getCoordinatesByFilter/')
//     .then(response => response.json())
//     .then(data => {
//         console.log(data);
//         // add data as markers to the map
//         for (var i = 0; i < data.length; i++) {
//             L.marker([data[i].latitud, data[i].longitud]).addTo(map);
//         }
//     })
//     .catch(error => {
//         // handle any errors that occur during the fetch request
//         console.error(error);
//     });