export class Tabs_View {
    constructor() {
        this.el_tabs = this.create_tabs_element();
    };
    create_tabs_element() {
        let el = document.createElement('div');
        el.classList.add('device-tabs');
        return el;        
    }
    add_tab(text) {
        let el = document.createElement('span');
        el.textContent = text;
        this.el_tabs.appendChild(el);
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
    get element() {
        return this.el_tabs;
    }
}