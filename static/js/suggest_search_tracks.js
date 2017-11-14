function clear(){
    var temp = new Array();
    for(i = 0; i < 5; i++){
        temp[i] = new Array();
    }
    return temp;
}

var last_query = "";
var current_suggestions = clear();

function fillhtmlsuggestions(){
    var result = "";
    var i;
    for(i = 0; i < 5; i++){
        var tmp = "";
        if(current_suggestions[i].length != 0){
            var name = current_suggestions[i][3] + " - " + current_suggestions[i][2] + " (add)";
            tmp = "<p onclick='addsong(" + i.toString() +")' class='suggestsuggestedsong'>" + name + "</p>";
        }
        result += tmp;
    }
    return result;
}

function fillsuggestions(query){
    $.post(
    "/search_tracks",
    $("#suggestsearch").serialize(),
    function(data){
        var tracks = JSON.parse(data);
        if(tracks.length == 0){
            current_suggestions = clear();
        }
        else{
            var i = 0;
            for(i = 0; i < tracks.length; i++){
                current_suggestions[i] = tracks[i];
            }
            for(;i < 5; i++){
                current_suggestions[i] = new Array();
            }
        }
        $("#suggestions").html(fillhtmlsuggestions());
        return 0;
    });
}

var losefocuscounter = 0;
function losefocus(){
    losefocuscounter += 1;
    var tmp = losefocuscounter;
    setTimeout(function(){
        if(tmp == losefocuscounter){
            current_suggestions = clear();
            $("#suggestions").html("");
        }
    }, 500);
}

function valuechange(){
    var current_query = $("#suggestsearchfield").val();
    if(current_query == last_query || current_query == ""){
        return 0;
    }
    last_query = current_query;
    setTimeout(function(){
        if(last_query == current_query){
            fillsuggestions(current_query);
        }
    }, 800);
    return false;
}

function focusing(){
    last_query = "";
    valuechange();
}