function empty_playlist(){
    temp = new Array();
    for(i = 0; i < 10; i++){
        temp[i] = new Array();
    }
    return temp;
}

var songscounter = 0;
var current_playlist = empty_playlist();

function addsong(i){
    if(songscounter < 10){
        for(j = 0; j < songscounter; j++){
            if(current_suggestions[i][0] == current_playlist[j][0]){
                return 0;
            }
        }
        current_playlist[songscounter] = current_suggestions[i];
        songscounter += 1;
        htmlplaylist();
    }
}

function htmlplaylist(){
    var result = "";
    for(i = 0; i < 10; i++){
        if(current_playlist[i].length == 0){
            $("#playlist").html(result);
            return 0;
        }
        var name = (i + 1).toString() + ".&nbsp;&nbsp;&nbsp;" + current_playlist[i][3] + " - " + current_playlist[i][2];
        result += "<p class='playlistsong'>" + name + "</p>";
        var frame = "<iframe src='https://open.spotify.com/embed?uri=" + current_playlist[i][1] + "' frameborder='0' allowtransparency='true' height='80'></iframe>";
        result += "<div class='suggestframediv'>" + frame + "</div>";
        result += "<div class='cls'></div>"
    }
    $("#playlist").html(result);
    return 0;
}

function clear_playlist(){
    current_playlist = empty_playlist();
    songscounter = 0;
    $("#playlist").fadeOut();
    hide_similar_different();
    setTimeout(function(){
        htmlplaylist();
        $("#playlist").fadeIn();
    }, 420);
}

function hide_similar_different(){
    $("#similarheader").fadeOut();
    $("#differentheader").fadeOut();
    $("#similar").html("");
    $("#different").html("");
}