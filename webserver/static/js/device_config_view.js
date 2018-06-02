import * as utilities from './utilities.js'

export class Device_Config_View {
    constructor() {
        // elements
        this.el_icon = this.create_device_icon_element();
        this.el_manufacturer_logo = this.create_manufacturer_logo_element();
        this.el_device_reference = this.create_device_reference_element();
        this.el_name = this.create_name_element();
        this.el_description = this.create_description_element();

        this.el_caption = this.create_caption_element();
        this.el_header = this.create_header_element();
        this.el_slots = this.create_slots_element();
        this.el_view = this.create_view();

        // events callbacks
        this._on_name_change = null;
    };
    set on_name_change(func) {
        this._on_name_change = func;
    }
    show(element_id) {
        var element = document.getElementById(element_id);
        element.innerHTML = '';
        element.appendChild(this.el_view);
    };
    set_slot(position, slot) {
        var slots = this.el_slots.childNodes;
        while (position>(slots.length-1)) {
            let el=document.createElement('div');
            el.classList.add('device-slot');
            this.el_slots.appendChild(el);
        }
        slots[position].replaceWith(slot);
    }
    /*************************************************************************
     * 
     */
    create_device_icon_element() {
        let el = document.createElement('img');
        el.classList.add('device-config-icon');
        return el;     
    };
    set device_icon(icon) {
        this.el_icon.src = utilities.gen_image_link(icon);
    }
    /*************************************************************************
     * 
     */
    create_manufacturer_logo_element() {
        let el = document.createElement('img');
        el.classList.add('device-config-manufacturer-logo');
        return el;
    };
    set manufacturer_logo(logo) {
        this.el_manufacturer_logo.src = utilities.gen_image_link(logo);
    };
    /*************************************************************************
     * 
     */
    create_device_reference_element() {
        let el = document.createElement('span');
        el.classList.add('device-config-device-reference');
        return el;
    };
    set device_reference(reference) {
        this.el_device_reference.textContent = reference;
    }
    /*************************************************************************
     * 
     */
    create_name_element() {
        let el = document.createElement('div');
        let view = this;
        el.spellcheck = false;    
        el.classList.add('device-config-name');
        el.contentEditable = true;
        el.addEventListener('keydown', event => {
            if (event.key == 'Enter') {
                event.stopImmediatePropagation();
                event.preventDefault();
                event.target.blur();
            }
        }, true);
        el.addEventListener('keypress', event => {
            if (event.key == 'Enter')
                event.stopImmediatePropagation();
        }, true);
        el.addEventListener('blur', event => {
            if (view._on_name_change!==null) 
                view._on_name_change(event.target.textContent);
        }, true);
        return el;
    }
    set name(name) {
        this.el_name.textContent = name;
    };
    /*************************************************************************
     * 
     */
    create_caption_element() {
        let el = document.createElement('div');
        el.classList.add('device-config-caption');
        el.appendChild(this.el_manufacturer_logo);
        el.appendChild(this.el_device_reference);
        el.appendChild(this.el_name);
        return el;
    }
    /*************************************************************************
     * 
     */
    create_header_element() {
        let el = document.createElement('div');
        el.classList.add('device-config-header');
        el.appendChild(this.el_icon);
        el.appendChild(this.el_caption);
        return el;
    }
    /*************************************************************************
     * 
     */
    create_description_element() {
        let el = document.createElement('div');
        el.classList.add('device-config-description');
        return el;
    };
    set_description(description) {
        this.el_description.textContent = description;
    }
    /*************************************************************************
     * 
     */
    create_slots_element() {
        let el = document.createElement('div');
        el.classList.add('device-slots');
        return el;
    }
    /*************************************************************************
     * 
     */
    create_view() {
        let el = document.createElement('div');
        el.classList.add('device-config');
        el.appendChild(this.el_header);
        el.appendChild(this.el_description);
        // only the slots container
        el.appendChild(this.el_slots);
        return el;
    }
}