google.charts.load('current', {'packages':['corechart', 'line']});
google.charts.setOnLoadCallback(drawChart);

function drawChart(){
    var data = new google.visualization.DataTable();
      data.addColumn('string', 'Day');
      data.addColumn('number', 'Guardians of the Galaxy');
      data.addColumn('number', 'The Avengers');
      data.addColumn('number', 'Transformers: Age of Extinction');

      data.addRows([
        ['kokoko1',  -37.8, -80.8, -41.8],
        ['2kokoko',  -30.9, -69.5, -32.4],
      ]);

      var options = {
         title: 'Box Office Earnings in First Two Weeks of Opening',
         subtitle: 'in millions of dollars (USD)',
         legend: { position: 'bottom' },
         width: 900,
        height: 500,
        backgroundColor: {
            fill: '#282828',
        },
        chartArea: {
            backgroundColor: '#282828',
        },
        fontName: "Abel",
        hAxis: {
            textStyle:{color: 'white'},
            gridlines: {
                color: 'white'
            }
        },
        vAxis: {
            textStyle:{color: 'white'},
            gridlines: {
                color: 'transparent'
            }
        },
        legend: {
            textStyle: {color: 'white'},
            position: "bottom",
        },
        titleTextStyle: {
            color: 'white',
        },
      }
       var chart = new google.visualization.LineChart(document.getElementById('linechart_material'));
       chart.draw(data, options);
}