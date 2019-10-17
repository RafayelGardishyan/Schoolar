 function processAjaxData(urlPath){
     document.getElementById("html").innerHTML = httpGet(urlPath);
     window.history.pushState({"html":httpGet(urlPath),"pageTitle":"Learn It"},"", urlPath);
 }

 window.onpopstate = function(e){
    if(e.state){
        document.getElementById("html").innerHTML = e.state.html;
    }
};

function httpGet(theUrl)
{
    var xmlHttp = new XMLHttpRequest();
    xmlHttp.open( "GET", theUrl, false ); // false for synchronous request
    xmlHttp.send( null );
    return xmlHttp.responseText;
}