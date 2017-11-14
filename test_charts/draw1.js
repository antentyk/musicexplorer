google.charts.load('current', {'packages':['corechart', 'line']});
google.charts.setOnLoadCallback(drawChart1);

function drawChart() {
    var data = google.visualization.arrayToDataTable([
        ['Year', 'Sales', 'Expenses'],
        ['2004 1st',  1000,      400],
        ['2005 1st',  1170,      460],
        ['2006 1st',  660,       1120],
        ['2007 1st',  1030,      540]
    ]);

    var options = {
        title: 'Company Performance',
        curveType: 'function',
        legend: { position: 'bottom' }
    };

    var chart = new google.visualization.LineChart(document.getElementById('curve_chart'));

    chart.draw(data, options);
}

function drawChart1(){
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
        chart: {
          title: 'Box Office Earnings in First Two Weeks of Opening',
          subtitle: 'in millions of dollars (USD)'
        },
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
      };

      /*var chart = new google.charts.Line(document.getElementById('linechart_material'));*/
      var chart = new google.visualization.LineChart(document.getElementById('linechart_material'));

    /*google.visualization.events.addListener(chart, 'ready', function () {
          var labels = document.getElementsByTagName('text');
          for (var i = 0; i < labels.length; i++) {
            if (labels[i].innerHTML === options.chart.subtitle) {
              labels[i].style.fill = 'white';
              labels[i].style.fontFamily = 'Abel';
              break;
            }
          }
        });*/

      chart.draw(data, options);
}