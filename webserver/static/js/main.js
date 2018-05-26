class TreeControl {
    constructor (container, tree_def){
        this.container = container;
        this.load(tree_def);
    };
    load(tree_def) {
        console.log(tree_def);
    };
}


function load_app(){
    var main_tree = document.getElementById('object-tree');
    var tree_def = [
        { 
            "caption": "System #0",
            "icon": "/static/images/house_icon.png",
            "data": { 
                "system-id": 0
            },
            "subtree": [
                {
                    "caption": "f454.sxpert.org",
                    "icon": "/static/images/F454_icon.png",
                },
                {
                    "caption": "devices",
                    "subtree": {
                        "onopen": load_devices,
                    }
                }
            ]
        }
    ]
    new TreeControl(main_tree, tree_def);
}


function ready(fn) {
    if (document.readyState === 'complete') {
        fn();
    } else {
        document.addEventListener('DOMContentLoaded', fn);
    }
}

ready(load_app);


