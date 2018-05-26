class TreeControl {
    constructor (container, tree_def){
        this.container = container;
        this.load(tree_def);
    };
    load(tree_def) {
        console.log(tree_def);
    };
}

class Gateway {
    constructor(gateway) {
        console.log(gateway)
    }
}

class System {
    constructor(system) {
        console.log(system)
        this.system_id = system.id;
        this.display_name = system.display_name;
        this.gateway = new Gateway(system.gateway)
    }
}

class App {
    constructor () {
        this.main_tree = new TreeControl("object-tree");
        this.content_pane = "main-content";
        this.systems = new Array();
    }; 
    load_main_tree(callback) {
        let app = this;
        let systems = this.systems;
        getJSON('/api/get-systems-list', function(tree_data) {
            tree_data.forEach(element => {
                var system = new System(element)
                systems.push(system)
            });
            console.log(systems);
            callback(app);
        });
    };
    start(){
        console.log('start the application');
        this.load_main_tree(this.initial_render);
    };
    initial_render(app) {
        console.log('render the application');
        app.initial_tree_render()
    };
    initial_tree_render() {
        console.log('start rendering the tree');
        console.log(this.systems);
        this.systems.forEach(element => {
            
        });
    };
}

Application = new App();

function load_app() {
    Application.start();
}

function getJSON(url, fn) {
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

function ready(fn) {
    if (document.readyState === "complete") {
        fn();
    } else {
        document.addEventListener("DOMContentLoaded", fn);
    }
}

ready(load_app);


