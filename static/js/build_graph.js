google.charts.load('current', {'packages':['corechart']});


var basic_options = {
        width: 1000,
        height: 200,
        backgroundColor: {fill: '#282828',},
        chartArea: {backgroundColor: '#282828',},
        fontName: "Abel",
        hAxis: {
            textStyle:{color: 'white'},
            gridlines: {color: 'white'}
        },
        vAxis: {
            textStyle:{color: 'white'},
            gridlines: {color: 'transparent'}
        },
        legend: {
            textStyle: {color: 'white'},
            position: "bottom",
        },
        titleTextStyle: {
            color: 'white',
        },
};

function build_all(graphs){
    $("#data").fadeOut();
    var result = "";
    for(i = 0; i < graphs.length; i++){
        result += "<div id='graph" + i.toString() + "'></div><div class='cls'></div>";
    }
    $("#graphs").html(result);
    for(i = 0; i < graphs.length; i++){
        graph = graphs[i];
        container_id = "graph" + i.toString();
        build(graph, container_id);
    }
}

var build(graph, container_id){
    var data = new google.visualization.DataTable();
    data.addColumn('string', 'Time');
    for(i = 0; i < graph["columns"].length; i++){
        data.addColumn('number', graph["columns"][i]);
    }
    data.addRows(graph["rows"]);
    var options = JSON.parse(JSON.stringify(basic_options));
    options.vAxis = jQuery.extend(options.vAxis, {minValue: graph["min"],
                                                  maxValue: graph["max"]});
    options.title = graph["title"];
    var chart = new google.visualization.LineChart(document.getElementById(container_id));
    chart.draw(data, options);
}