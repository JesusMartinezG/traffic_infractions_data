var map = L.map('map').setView(
    [19.381074826513803, -99.13842300487916], 12
    );

// set map's minimum zoom
map.setMinZoom(10);
// lock map boundries
map.setMaxBounds([
    [19.660760188533505, -99.41937189586469],
    [19.058925309976264, -98.8522535751143]
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
// var asHeatmap = document.getElementById('asHeatmap');
// var filtersInput = document.getElementById('filters');
// var asCluster = document.getElementById('asCluster');

var keys = ['dia_semana', 'tipo_incidente_c4', 'incidente_c4', 'clas_con_f_alarma', 'tipo_entrada', 'alcaldia_inicio', 'inicio', 'final', 'limit'];

var inputs = {
    dia_semana: document.getElementById('dia_semana'),
    tipo_incidente_c4: document.getElementById('tipo_incidente_c4'),
    incidente_c4: document.getElementById('incidente_c4'),
    clas_con_f_alarma: document.getElementById('clas_con_f_alarma'),
    tipo_entrada: document.getElementById('tipo_entrada'),
    alcaldia_inicio: document.getElementById('alcaldia_inicio'),
    inicio: document.getElementById('inicio'),
    final: document.getElementById('final'),
    limit: document.getElementById('limit')
}
// var limitInput = document.getElementById('limit');

apply.addEventListener('click', function() {
    var arguments = [];
    //get the values from input fields
    for (var key of keys) {
        if (inputs[key].value != '') {
            arguments.push(key + '=' + inputs[key].value);
        }
    }

    // Join the arguments into a single string
    var filters = '';
    if (arguments.length > 0) {
        filters = arguments.join('&');
    }

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
                    mark.bindPopup("<b>"+data[i].tipo+": "+data[i].folio+"</b><br><div style='text-align: center; width: 100%'>"+data[i].creacion+"</div>");
                    markers.addLayer(mark);
                }
                markers.addTo(map);
            })
            .catch(error => {
                // handle any errors that occur during the fetch request
                console.error(error);
            });
    }
    else{
        fetch('api/getCoordinatesByFilter/')
            .then(response => response.json())
            .then(data => {
                var markers = L.markerClusterGroup();
                for (var i = 0; i < data.length; i++) {
                    var mark = L.marker([data[i].latitud, data[i].longitud]);
                    mark.bindPopup("<b>"+data[i].tipo+"</b><br>"+data[i].creacion);
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

// asHeatmap.addEventListener('click', function() {
//     //get the values from input field
//     filters = filtersInput.value;
//     //if filters is not empty
//     if (filters) {
//         //remove all markers
//         map.eachLayer(function(layer) {
//             if (layer instanceof L.Marker || layer instanceof HeatmapOverlay || layer instanceof L.MarkerCluster) {
//                 map.removeLayer(layer);
//             }
//         })
//         //call api endpoint to get coordinates
//         fetch('api/getCoordinatesByFilter/?' + filters)
//             .then(response => response.json())
//             .then(data => {
//                 var heatmapData = {
//                     max: data.length,
//                     min: data.length/10,
//                     data: data
//                 };
//                 cfg.radius= Math.min(5/data.length, 0.006);
//                 var heatmapLayer = new HeatmapOverlay(cfg);
//                 heatmapLayer.setData(heatmapData);
//                 heatmapLayer.addTo(map);
//             })
//             .catch(error => {
//                 // handle any errors that occur during the fetch request
//                 console.error(error);
//             });
//     }
// })

// asCluster.addEventListener('click', function() {
//     //get the values from input field
//     filters = filtersInput.value;
//     //if filters is not empty
//     if (filters) {
//         //remove all markers
//         map.eachLayer(function(layer) {
//             if (layer instanceof L.Marker || layer instanceof HeatmapOverlay || layer instanceof L.MarkerCluster) {
//                 map.removeLayer(layer);
//             }
//         })
//         //call api endpoint to get coordinates
//         fetch('api/getCoordinatesByFilter/?' + filters)
//             .then(response => response.json())
//             .then(data => {
//                 var markers = L.markerClusterGroup();
//                 for (var i = 0; i < data.length; i++) {
//                     var mark = L.marker([data[i].latitud, data[i].longitud]);
//                     markers.addLayer(mark);
//                 }
//                 markers.addTo(map);
//             })
//             .catch(error => {
//                 // handle any errors that occur during the fetch request
//                 console.error(error);
//             });
//     }
// })

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