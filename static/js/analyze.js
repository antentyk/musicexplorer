function handle_quarter_year_change(){
    var tmp = $("#time_type").val();
    if(tmp == "years"){
        $("#quarters_special_div").fadeOut(800);
        var start = 1956;
    }
    else{
        $("#quarters_special_div").fadeIn(800);
        var start = 2010;
    }
    var result = "";
    for(i = start; i < 2017; i++){
        var n = i.toString();
        result += "<option value='" + n + "'> " + n + " </option>";
    }
    $("#start_year").html(result);
    var result = "";
    for(i = start + 1; i <= 2017; i++){
        var n = i.toString();
        result += "<option value='" + n + "'> " + n + " </option>";
    }
    $("#end_year").html(result);
    $("#start_year_div").fadeIn(800);
    $("#end_year_div").fadeIn(800);
    handle_end_year();
}

function change_end_year(){
    var tmp = parseInt($("#start_year").val());
    var result = "";
    for(i = tmp + 1; i <= 2017; i++){
        var n = i.toString();
        result += "<option value='" + n + "'> " + n + " </option>";
    }
    $("#end_year").html(result);
}

function handle_end_year(){
    var tmp = $("#end_year").val();
    if(tmp == null || tmp <= parseInt($("#start_year").val())){
        $("#end_year_div").fadeTo(200, 0);
        setTimeout(function(){
            change_end_year();
            $("#end_year_div").fadeTo(200, 1);
        }, 500);
    }
}

$(document).ready(function() {
    handle_quarter_year_change();
    handle_end_year();
});

var characteristics = ["acousticness",
                       "danceability",
                       "energy",
                       "instrumentalness",
                       "speechiness",
                       "valence",
                       "duration_ms",
                       "loudness",
                       "tempo"];

function check_data(){
    for(i = 0; i < characteristics.length; i++){
        if($("#" + characteristics[i] + "_check").is(':checked')){
            return true;
        }
    }
    return false;
}

var sended = false;

function send(){
    if(!sended && check_data()){
        sended = true;
        console.log($("#criterias").serialize());
        $.ajax({
            type : "POST",
            url : "/get_graphs_data",
            data: $("#criterias").serialize(),
            success: function(result) {
                console.log(result);
                result = JSON.parse(result);
                console.log(result);
                google.charts.load('current', {
                    callback: function () {
                        $("#data").fadeOut();
                        var htmlcode = "";
                        for(i = 0; i < result.length; i++){
                            htmlcode += "<div id='graph" + i.toString() + "'></div><div class='cls'></div>";
                        }
                        $("#graphs").html(htmlcode);
                        for(i = 0; i < result.length; i++){
                            var graph = result[i];
                            var container_id = "graph" + i.toString();
                            var data = new google.visualization.DataTable();
                            data.addColumn('string', 'Time');
                            for(j = 0; j < graph["columns"].length; j++){
                                data.addColumn('number', graph["columns"][j]);
                            }
                            data.addRows(graph["rows"]);
                            var options = JSON.parse(JSON.stringify(basic_options));
                            options.vAxis = jQuery.extend(options.vAxis, {minValue: graph["min"],
                                                                          maxValue: graph["max"]});
                            options.title = graph["title"];
                            var chart = new google.visualization.LineChart(document.getElementById(container_id));
                            chart.draw(data, options);
                        }
                    },
                    packages: ['corechart']
                });
            }
        });
    }
    return false;
}

var basic_options = {
        width: $(window).width(),
        height: 700,
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
        curveType: 'function',
};