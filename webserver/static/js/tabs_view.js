export class Tabs_View {
    constructor() {
        this._on_click = null;
        this.el_tabs = this.create_tabs_element();
    };
    set on_click(func) {
        this._on_click = func;
    }
    create_tabs_element() {
        let el = document.createElement('div');
        el.classList.add('device-tabs');
        return el;        
    }
    add_tab(id, text) {
        let el = document.createElement('span');
        el.textContent = text;
        this.el_tabs.appendChild(el);
        let view = this;
        el.addEventListener('click', event => {
            if (view._on_click!==null) 
                view._on_click(id);
        });
    }
    select_tab(id) {
        let children = this.el_tabs.childNodes;
        var c = 0;
        for(let child of children) {
            if (c == id)
                child.classList.add('selected');
            else    
                child.classList.remove('selected');
            c++;
        }
    }
    change_tab_width(tab_index, width) {
        let children = this.el_tabs.childNodes;
        if (tab_index<children.length) {
            // show everything again
            for(var child of children) {
                child.hidden = false;
            }
            var tab = children[tab_index];
            tab.style.flexGrow = width;
            tab.style.flexShrink = width;
            tab.style.flexBasis = 0;
            var ch = width-1;
            // hide the necessary slots
            while(ch>0) {
                tab = tab.nextSibling;
                tab.hidden = true;
                ch--;
            }
        }
    }
    change_tab_label(tab_index, tab_label) {
        let children = this.el_tabs.childNodes;
        let tab = children[tab_index];
        tab.textContent = tab_label;
    }
    get element() {
        return this.el_tabs;
    }
}