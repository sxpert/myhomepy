import * as utilities from './utilities.js'

export class Device_Config_View {
    constructor() {
        // buttons
        this.el_discover = null;
        this.el_discover = null;

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
        this._on_discover_request = null;
        this._on_program_request = null;
    };
    set on_name_change(func) {
        this._on_name_change = func;
    }
    set on_discover_request(func) {
        this._on_discover_request = func;
    }
    set on_program_request(func) {
        this._on_program_request = func;
    }
    set enabled(enabled) {
        this.el_discover.disabled = !enabled;
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
        let view = this;
        let el = document.createElement('div');
        el.classList.add('device-config-caption');
        let buttons = document.createElement('div');
        buttons.classList.add('device-config-buttons');
        this.el_discover = document.createElement('button');
        this.el_discover.classList.add('device-config-button');
        this.el_discover.textContent='Device Discover';
        this.el_discover.addEventListener('click', event => {
            console.log('discover pressed');
            if (view._on_discover_request!==null) 
                view._on_discover_request();
        }, true);
        this.el_program = document.createElement('button');
        this.el_program.classList.add('device-config-button');
        this.el_program.textContent='Program Device';
        this.el_program.addEventListener('click', event => {
            console.log('program pressed');
            if (view._on_program_request!==null) 
                view._on_program_request();
        }, true);
        buttons.appendChild(this.el_discover);
        buttons.appendChild(this.el_program);
        el.appendChild(buttons);
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