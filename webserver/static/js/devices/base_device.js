
export class Base_Slot {
    constructor(device, data) {
        console.log('Base_Slot::constructor');
        console.log(data);
        this.device = device;
        this.number = device.slots.indexOf(this);
        this.data = data;
        this.options = data.options;
        // this needs to be done before fscking with the fields
        this.values = data.values;
        this.params = data.params;
        // create the ordered dataset
        this.fields = this.options.fields;
        if ((this.fields !== undefined) && (Array.isArray(this.fields))) {
            var ordered = [];
            var dict = {};
            for(var f=0; f<this.fields.length; f++) {
                var field = this.fields[f];
                if (ordered[field.order]===undefined)
                    ordered[field.order] = [];
                ordered[field.order].push(field);
                dict[field.name] = field;
                this.set_behavior(field);
            }
            var fields = {};
            fields.ordered = ordered;
            fields.dict = dict;
            this.fields = fields;
        } else
            console.log('WARNING: Expected data.options.fields to be an Array instance');
    };
    slot_elements(){
        console.log('Base_slot::slot_elements ', this.options);
        var sl = document.createElement('div');
        sl.classList.add('device-slot');
        // loops on each field and get it's main element back
        // each field is primed with it's own events
        for(var i=0; i<this.fields.ordered.length; i++){
            var layer = this.fields.ordered[i];
            console.log(layer);
        }

    };
    //------------------------------------------------------------------------
    //
    // Field helper functions
    //
    //
    get_value(fieldname) {
        return this.values[fieldname];
    };
    set_value(fieldname, value) {
        // updates the value for the field
        // then calls each field to get it to show/hide itself
    };
    //------------------------------------------------------------------------
    //
    // Major javascript object hacking
    //
    //
    set_behavior(field) {
        switch (field.type) {
            case 'select': this.set_select_behavior(field); break;
        }
    };
    set_select_behavior(field) {
        let slot = this;
        field.elements = function() {
            var ct = document.createElement('div');
            var lb = document.createElement('label');
            lb.textContent = this.name;
            var sl = document.createElement('select');
            console.log(slot.get_value(this.name));
        };
    };
}


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
        el.textContent = 'slots';
        return el;
    };
}