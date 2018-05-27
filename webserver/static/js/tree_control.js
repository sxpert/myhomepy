import * as utilities from './utilities.js'

export class TreeControl {
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

export class TreeItem {
    constructor (label, icon=null) {
        this.label = label;
        this.icon = icon;
        this.items = new Array();
        this.dom_element = null;
        this.de_header = null;
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
                return utilities.gen_image_link('arrow-open');
            } else {
                return utilities.gen_image_link('arrow-closed');
            }
        } else {
            return utilities.gen_image_link('blank');
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
            this.de_header = document.createElement('div');
            this.de_header.classList.add('tree-header');

            this.de_arrow = document.createElement('img');
            this.de_arrow.classList.add('tree-arrow');
            this.de_arrow.addEventListener('click', function() {
                tree.toggle_tree() 
            });
            this.de_arrow.src = this.get_arrow_icon();
            this.de_header.appendChild(this.de_arrow);
            
            this.de_icon = document.createElement('img');
            this.de_icon.classList.add('tree-icon');
            var icon = utilities.gen_image_link(this.get_icon());
            if (icon === null) {
                icon = utilities.gen_image_link('blank');
            }
            this.de_icon.src = icon;
            this.de_header.appendChild(this.de_icon);
            
            this.de_label = document.createElement('span');
            this.de_label.textContent = this.label;
            this.de_header.appendChild(this.de_label);
            if (this.on_click_func !== null) {
                this.de_header.addEventListener('click', this.on_click_func);
            }
            el.appendChild(this.de_header);

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
        if (this.de_header !== null) {
            this.de_header.addEventListener('click', func)
        } 
    }
}

