export function get_json(url, fn) {
    var request = new XMLHttpRequest();
    request.open("GET", url, true);
    request.onload = function() {
        if (request.status >= 200 && request.status < 400) {
            var data = JSON.parse(request.responseText);
            fn(data);
        } else {
            console.log('onload : some error occured');
            console.log(request);
        }
    };
    request.onerror = function(){
        console.log('onerror : some error occured');
        console.log(request);
    };
    request.send();
}
