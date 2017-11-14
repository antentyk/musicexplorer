var last_playlist = empty_playlist();

function equal(first_playlist, second_playlist){
    for(i = 0; i < 10; i++){
        var a = first_playlist[i].length;
        var b = second_playlist[i].length;
        if(a == b){
            if(a != 0){
                if(first_playlist[i][0] != second_playlist[i][0]){
                    return false;
                }
            }
        }
        else{
            return false;
        }
    }
    return true;
}

var last_result;
var last_result_playlist = empty_playlist();

function show_similar_different_result(){
    $("#loading").fadeOut();
    $("#differentheader").fadeIn();
    $("#similarheader").fadeIn();
    htmlsimilardifferent(last_result["similar"], last_result["different"])
}

function send_playlist(){
    if(equal(current_playlist, empty_playlist())){
        return 1;
    }
    if(equal(current_playlist, last_result_playlist)){
        show_similar_different_result();
        return 0;
    }
    last_playlist = current_playlist;
    $("#loading").fadeIn();
    var data = {};
    data["playlist"] = current_playlist;
    last_result_playlist = current_playlist.slice();
    hide_similar_different();
    $.ajax({
    type : "POST",
    url : "/find_closest",
    data: JSON.stringify(data),
    contentType: 'application/json;charset=UTF-8',
    success: function(result) {
        last_result = JSON.parse(result);
        show_similar_different_result();
    }
});
}

function htmlsimilardifferent(similar, different){
    var resultsimilar = "";
    var resultdifferent = "";
    for(i = 0; i < 5; i++){
        var names = (i + 1).toString() + ".&nbsp;&nbsp;&nbsp;" + similar[i][3] + " - " + similar[i][2];
        resultsimilar += "<p class='playlistsong'>" + names + "</p>";
        var named = (i + 1).toString() + ".&nbsp;&nbsp;&nbsp;" + different[i][3] + " - " + different[i][2];
        resultdifferent += "<p class='playlistsong'>" + named + "</p>";
        var frames = "<iframe src='https://open.spotify.com/embed?uri=" + similar[i][1] + "' frameborder='0' allowtransparency='true' height='80'></iframe>";
        resultsimilar += "<div class='suggestframediv'>" + frames + "</div>";
        resultsimilar += "<div class='cls'></div>"
        var framed = "<iframe src='https://open.spotify.com/embed?uri=" + different[i][1] + "' frameborder='0' allowtransparency='true' height='80'></iframe>";
        resultdifferent += "<div class='suggestframediv'>" + framed + "</div>";
        resultdifferent += "<div class='cls'></div>";
    }
    $("#similar").html(resultsimilar);
    $("#different").html(resultdifferent);
    return 0;
}