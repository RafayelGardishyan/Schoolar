 function processAjaxData(response, urlPath, title){
     document.getElementById("html").innerHTML = response;
     window.history.pushState({"html":response.html,"pageTitle":"Learn It"},"", urlPath);
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