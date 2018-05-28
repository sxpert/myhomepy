import * as utilities from './utilities.js'

export class Device_Config_Page {
    constructor(element_id) {
        this.element_id = element_id;
        this.element = document.getElementById(this.element_id);
        this.device = null;
        this.el_page = null;
        this.el_header = null;
        this.el_icon = null;
        this.el_manufacturer_logo = null;
        this.el_device_reference = null;
        this.el_name = null;
        this.name_empty = true;
        this.el_caption = null;
        this.el_description = null;
        this.description_empty = true;
        this.el_slots = null;
    };
    set_device(device) {
        this.device = device;
        this.setup_html_controls();
    };
    setup_html_controls() {
        this.el_icon = document.createElement('img');
        this.el_icon.classList.add('device-config-icon');
        this.el_icon.src = utilities.gen_image_link(this.device.icon);

        console.log('manufacturer "'+this.device.manufacturer+'"');
        if (this.device.manufacturer === null) {
            console.log('manufacturer is js::null');
            this.el_manufacturer_logo = document.createElement('span');
            this.el_manufacturer_logo.textContent = 'Unknown'
        } else {
            this.el_manufacturer_logo = document.createElement('img');
            this.el_manufacturer_logo.src = utilities.gen_image_link(this.device.manufacturer);
        }
        this.el_manufacturer_logo.classList.add('device-config-manufacturer-logo');

        this.el_device_reference = document.createElement('span');
        this.el_device_reference.classList.add('device-config-device-reference');
        this.el_device_reference.textContent = this.device.device_reference;

        this.el_name = document.createElement('div');
        this.el_name.classList.add('device-config-name');

        this.el_caption = document.createElement('div');
        this.el_caption.classList.add('device-config-caption');
        this.el_caption.appendChild(this.el_manufacturer_logo);
        this.el_caption.appendChild(this.el_device_reference);
        this.el_caption.appendChild(this.el_name);

        this.el_header = document.createElement('div');
        this.el_header.classList.add('device-config-header');
        this.el_header.appendChild(this.el_icon);
        this.el_header.appendChild(this.el_caption);

        this.el_description = document.createElement('div');
        this.el_description.classList.add('device-config-description');
        var description = this.device.description;

        this.el_slots = this.device.slots_elements();

        this.el_page = document.createElement('div');
        this.el_page.classList.add('device-config');
        this.el_page.appendChild(this.el_header);
        this.el_page.appendChild(this.el_description);
        this.el_page.appendChild(this.el_slots);

        this.element.innerHTML = '';
        this.element.appendChild(this.el_page);

        this.set_name();
        this.set_description();
    };
    set_name() {
        var name = this.device.name;
        console.log('name "'+name+'"');
        if (name.length == 0) {
            this.name_empty = true;
            name = this.device.id;
        } else
            this.name_empty = false;
        this.el_name.textContent = name;
    };
    set_description() {
        var description = this.device.description;
        console.log('description "'+description+'"');
        if (description.length == 0) {
            this.description_empty = true;
            description = 'enter some description';
        } else
            this.description_empty = false;
        this.el_description.textContent = description;
    }
}