var ishidden = true;
var counter = 0;

function change(){
    counter += 1;
    var tmp = counter;
    if(ishidden){
        setTimeout(function(){
        if(tmp == counter){
            $("#suggestinfodiv").fadeIn();
            $("#suggestinfosign").attr("src","../static/photo/minus.png");
            ishidden = false;
        }
        }, 400);
    }
    else{
        setTimeout(function(){
        if(tmp == counter){
            $("#suggestinfodiv").fadeOut();
            $("#suggestinfosign").attr("src","../static/photo/plus.png");
            ishidden = true;
        }
        }, 400);
    }
}