
/**
 * Listens for a request from the button in the browser.
 * When it sees the getSelection request, it returns the selection HTML, as well as the URL and title of the tab.
 */
document.addEventListener('mouseup',function(event){
    var sel = window.getSelection().toString();
    var elem = event.srcElement;
    if(sel.length > 5)
        chrome.extension.sendRequest({'message':'setText','data': sel, "elem" : elem.id},function(response){
        })
});