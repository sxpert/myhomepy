class Slot_4652 {
    constructor (data) {
        console.log(data);
    };
}

let dev_types = {
    2 : {
        nb_slots : 2,
        references : {
            'BRAND_UNDEFINED' : {
                0 : '<unknown>'
            },
            'BRAND_BTICINO' : {
                3 : 'H4652/2'
            },
            'BRAND_LEGRAND' : {
                4 : '067552'
            }
        }
    }
}

export class Device_4652 {
    constructor(data, config_page) {
        this.config_page = config_page;
        console.log(data);
        this.icon = data.icon;
        this.id = data.id;
        this.name = data.name;
        this.description = data.description;
        this.brand_id = data.brand_id;
        this.product_line = data.product_line;
        this.subsystem = data.subsystem;
        this.model_id = data.model_id;

        this.set_device_reference();

        if (this.model_id == 2) {
            this.slots = new Array(2);
            
        }
        for(var i=0; i < this.slots.length; i++)
            this.slots[i] = new Slot_4652(data.slots[i]);
        console.log(this.slots);
        this.setup_config_page();
    };
    set_device_reference() {
        let model = dev_types[this.model_id];
        console.log('model', model);
        if (model!==undefined) {
            let refs = model.references;
            console.log('refs', refs);
            if (refs!==undefined) {
                let brand = refs[this.brand_id];
                console.log('brand', brand);
                if (brand!==undefined) {
                    let ref = brand[this.product_line]
                    console.log('ref', ref);
                    if (ref!==undefined) {
                        this.device_reference = ref;
                        return;
                    }
                }
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