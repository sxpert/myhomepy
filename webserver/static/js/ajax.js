export function get_json(url, success=null, error=null) {
    var request = new XMLHttpRequest();
    request.open("GET", url, true);
    request.onload = function() {
        if (request.status >= 200 && request.status < 400) {
            var data = JSON.parse(request.responseText);
            if (success !== null) {
                success(data);
            }
        } else {
            if (error !== null) {
                error(request);
            } else {
                console.log('onload : some error occured');
                console.log(request);
            }
        }
    };
    request.onerror = function(){
        if (error !== null) {
            error(request);
        } else {
            console.log('onerror : some error occured');
            console.log(request);    
        }
    };
    request.send();
}
