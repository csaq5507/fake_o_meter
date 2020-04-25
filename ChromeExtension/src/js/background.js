chrome.runtime.onInstalled.addListener(function() {
    chrome.storage.sync.set({color: '#3aa757'}, function() {
        console.log("The color is green.");
    });

});

var seltext = null;

chrome.extension.onRequest.addListener(function(request, sender, sendResponse)
{
    switch(request.message)
    {
        case 'setText':
            window.seltext = request.data
            break;

        default:
            sendResponse({data: 'Invalid arguments'});
            break;
    }
});


function savetext(info,tab)
{
    var jax = new XMLHttpRequest();
    jax.open("POST","http://fakt.kalle.click");
    jax.setRequestHeader("Content-Type","application/x-www-form-urlencoded");
    jax.send("text="+seltext);
    jax.onreadystatechange = function() { if(jax.readyState==4) {
        alert(jax.responseText);
    }}
}

var contexts = ["selection"];
for (var i = 0; i < contexts.length; i++)
{
    var context = contexts[i];
    chrome.contextMenus.create({"title": "Is this fake-news?", "contexts":[context], "onclick": savetext});
}
