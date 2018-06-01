import * as base_slot from './base_slot.js';

export class Base_Device {
    constructor(data, config_page) {
        this.config_page = config_page;
        this.icon = data.icon;
        this.id = data.id;
        this.name = data.name;
        this.description = data.description;
        this.brand_id = data.brand_id;
        this.manufacturer = null;
        this.user_can_set_brand = false;
        this.user_set_brand = null;
        this.product_line = data.product_line;
        this.user_can_set_product_line = false;
        this.user_set_product_line = null;
        this.subsystem = data.subsystem;
        this.model_id = data.model_id;
        this.dev_types = null;
    }
    setup_slots(data) {
        // setup slots
        var slot_class = base_slot.Base_Slot;
        if (this.slot_class!==undefined)
            slot_class = this.slot_class;
        var nb_slots = 0;
        if (this.nb_slots!==undefined) 
            nb_slots = this.nb_slots;
        this.slots = new Array(nb_slots);
        for(var i=0; i < this.slots.length; i++)
            this.slots[i] = new slot_class(this, data.slots[i]);
    };
    set_device_reference() {
        let model = this.dev_types[this.model_id];
        if (model!==undefined) {
            let refs = model.references;
            if (refs!==undefined) {
                let brand = refs[this.brand_id];
                if (this.brand_id == 'BRAND_UNDEFINED') {
                    this.user_can_set_brand = true;
                    brand = undefined;
                } else 
                    this.manufacturer = brand.icon;
                if (brand!==undefined) {
                    let ref = brand[this.product_line]
                    if (ref!==undefined) {
                        this.device_reference = ref;
                        return;
                    }
                }
                this.user_can_set_product_line = true;
            }
        }
        this.device_reference = '<unknown>';
    }
    setup_config_page() {
        this.config_page.set_device(this);
    };
    slots_elements() {
        var el = document.createElement('div');
        el.classList.add('device-slots');
        for(var i=0; i<this.slots.length;i++) {
            var slot_el = this.slots[i].slot_elements();
            if ((slot_el !== undefined) && (slot_el !== null))
                el.appendChild(slot_el);
        }
        return el;
    };
}