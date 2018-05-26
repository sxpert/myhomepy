function gen_image_link(item) {
    return '/static/images/'+item+'_icon.png';
}

class TreeControl {
    // this TreeControl contains multiple TreeItem
    // 
    constructor (container){
        this.items = new Array()
        this.container = container
        this.dom_element = null;
    };
    add_item(item) {
        if (item !== null){
            this.items.push(item);
            var element = item.get_dom_element();
            this.get_dom_element().appendChild(element);
        }
    }
    get_dom_element() {
        if (this.dom_element === null) {
            var el = document.getElementById(this.container);
            this.dom_element = el;
        }
        return this.dom_element;
    }
}

class TreeItem {
    constructor (label, icon=null) {
        this.label = label;
        this.icon = icon;
        this.items = new Array();
        this.dom_element = null;
        this.de_arrow = null;
        this.de_icon = null;
        this.de_label = null;
        this.on_click_func = null;
        this.de_items = null;
        this.open = false;
    };
    append_item(item) {
        if (item !== null) {
            this.items.push(item);
            this.update_arrow();
            if (this.de_items === null) {
                this.get_dom_element();
            }
            var el = item.get_dom_element()
            this.de_items.appendChild(el);
        }
    };
    empty() {
        this.items = new Array();
        this.de_items.innerHTML='';
    }
    get_arrow_icon() {
        if (this.items.length > 0) {
            if (this.open) {
                return gen_image_link('arrow-open');
            } else {
                return gen_image_link('arrow-closed');
            }
        } else {
            return gen_image_link('blank');
        }
    };
    get_icon() {
        var icon = this.icon;
        if (icon === null) {
            icon = 'blank';
        }
        return icon;
    }
    update_arrow() {
        if (this.de_arrow === null) {
            return;
        }
        this.de_arrow.src = this.get_arrow_icon()
    }
    toggle_tree() {
        this.open = !this.open;
        this.update_arrow();
        this.de_items.style.display = this.open ? 'block' : 'none';
    }
    get_dom_element() {
        let tree = this;
        if (this.dom_element === null) {
            // create the dom element
            var el = document.createElement('div');
            el.classList.add('tree-item');
            this.de_arrow = document.createElement('img');
            this.de_arrow.classList.add('tree-arrow');
            this.de_arrow.addEventListener('click', function() {
                tree.toggle_tree() 
            });
            this.de_arrow.src = this.get_arrow_icon();
            el.appendChild(this.de_arrow);
            this.de_icon = document.createElement('img');
            this.de_icon.classList.add('tree-icon');
            var icon = gen_image_link(this.get_icon());
            if (icon === null) {
                icon = gen_image_link('blank');
            }
            this.de_icon.src = icon;
            el.appendChild(this.de_icon);
            this.de_label = document.createElement('span');
            this.de_label.textContent = this.label;
            if (this.on_click_func !== null) {
                this.de_label.addEventListener('click', this.on_click_func);
            }
            el.appendChild(this.de_label);
            this.de_items = document.createElement('div');
            this.de_items.classList.add('tree');
            if (!this.open) {
                this.de_items.style.display = 'none';
            }
            if (this.items.length > 0) {
                this.items.forEach(item => {
                    this.de_items.appendChild(item.get_dom_element());
                });
            }
            el.appendChild(this.de_items);
            this.dom_element = el;
        }
        return this.dom_element;
    };
    set_icon(icon) {
        console.log('TreeItem::set_icon', icon);
    };
    on_click(func) {
        this.on_click_func = func
        if (this.de_label !== null) {
            this.de_label.addEventListener('click', func)
        } 
    }
}

class Gateway {
    constructor(gateway) {
        this.tree_item = null;
        this.display_name = gateway.display_name;
        this.model = gateway.model;
    };
    get_tree_item() {
        if (this.tree_item === null) {
            var item = new TreeItem(this.display_name, this.model);
            this.tree_item = item;
        }
        return this.tree_item;
    }
}

class Device {
    constructor(devices, data) {
        this.tree_item = null;
        this.devices = devices;
        this.label = data.id;
        this.icon = data.icon;
    };
    get_tree_item() {
        if (this.tree_item === null) {
            var item = new TreeItem(this.label, this.icon);
            var device = this;
            var click_func = function() {
                device.click();
            }
            item.on_click(click_func);
            this.tree_item = item;
        }
        return this.tree_item;
    };
    click() {
        console.log(this.label, 'clicked')
    }
}

class Devices {
    constructor(system) {
        this.tree_item = null;
        this.system = system;
        this.devices = []
    }
    get_tree_item() {
        if (this.tree_item === null) {
            var devices = this
            var item = new TreeItem('Devices');
            this.tree_item = item;
            get_json('/api/get-system-devices?system_id='+this.system.system_id,
                function(data) {
                    if (data.ok !== undefined && data.ok === true) {
                        devices.update_device_list(data);
                    }
                });
        }
        return this.tree_item;
    }
    update_device_list(devices){
        if ((devices.ok !== undefined) && (devices.ok)){
            devices = devices.devices;
            this.devices = [];
            this.tree_item.empty()
            devices.forEach(data => {
                var device = new Device(this, data);
                this.devices.push(device);
                var elem = device.get_tree_item();
                this.tree_item.append_item(elem);
            });
        }

    }
}

class System {
    constructor(system) {
        this.tree_item = null;
        this.system_id = system.id;
        this.display_name = system.display_name;
        this.gateway = new Gateway(system.gateway)
        this.devices = new Devices(this);
    }
    get_tree_item() {
        if (this.tree_item === null) {
            var item = new TreeItem(this.display_name, 'house');
            item.append_item(this.gateway.get_tree_item());
            item.append_item(this.devices.get_tree_item());
            this.tree_item = item;
        }
        return this.tree_item;
    }
    update_devices() {

    }
}

class App {
    constructor () {
        this.main_tree = new TreeControl("object-tree");
        this.content_pane = "main-content";
        this.systems = new Array();
    }; 
    start(){
        let app = this;
        let systems = this.systems;
        get_json('/api/get-systems-list', function (data) {
            data.forEach(sys_data => {
                var system = new System(sys_data);
                app.add_system(system);
            });
        });
    };
    add_system(system) {
        if (system !== null) {
            this.systems.push(system);
            var item = system.get_tree_item();
            this.main_tree.add_item(item);
        }
    };
}

Application = new App();

function load_app() {
    Application.start();
}

function get_json(url, fn) {
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


