chrome.runtime.onInstalled.addListener(function() {
    chrome.storage.sync.set({color: '#3aa757'}, function() {
        console.log("The color is green.");
    });

});

var seltext = null;
var selElemId = null;


chrome.extension.onRequest.addListener(function(request, sender, sendResponse)
{
    switch(request.message)
    {
        case 'setText':
            window.seltext = request.data;
            window.selElemId = request.elem;
            console.log(request.elem);
            break;

        default:
            sendResponse({data: 'Invalid arguments'});
            break;
    }
});


function savetext(info,tab)
{
    var jax = new XMLHttpRequest();
    jax.open("POST","https://fakt.kalle.click");
    jax.setRequestHeader("Content-Type","application/x-www-form-urlencoded");
    jax.send("text="+seltext);
    jax.onreadystatechange = function() { if(jax.readyState==4) {
      /*  let img = document.createElement("div");
        img.src="res/green.jpg";
        img.alt=jax.responseText;
        let elem = document.getElementById(window.selElem);
        console.log(elem);
        if(window.selElem!== null)
            elem.append(img);
        else
            document.getElementsByTagName("body")[0].append(img);
*/
        alert(jax.responseText);

    }}
}

var contexts = ["selection"];
for (var i = 0; i < contexts.length; i++)
{
    var context = contexts[i];
    chrome.contextMenus.create({"title": "Is this fake-news?", "contexts":[context], "onclick": savetext});
}
