var TESTER = document.getElementById('tester');
Plotly.newPlot( TESTER, [{
x: [1, 2, 3, 4, 5],
y: [1, 2, 4, 8, 16] }], {
margin: { t: 0 } } );

var barChart = document.getElementById('barChart');
var showDataButton = document.getElementById('showData');
// var data;
// data = {
//     x: ['giraffes', 'orangutans', 'monkeys'],
//     y: [20, 14, 23],
//     type: 'bar'
//   }

showDataButton.addEventListener('click', function() {
    fetch('api/getBarChartData')
    .then(response => response.json())
    .then(data => {
        console.log(data);
        Plotly.react( barChart, [data]);
    })
    .catch(error => {
        // handle any errors that occur during the fetch request
        console.error(error);
    })
})

Plotly.newPlot( barChart, [{}]);