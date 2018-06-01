import * as base from './base_device.js';

let dev_types = {
    2 : {
        nb_slots : 2,
        references : {
            'BRAND_UNDEFINED' : {
                0 : '<unknown>'
            },
            'BRAND_BTICINO' : {
                icon: 'BTicino',
                3 : 'Axolute H4652/2'
            },
            'BRAND_LEGRAND' : {
                icon: 'Legrand',
                4 : 'Céliane 067552'
            }
        }
    }
}

export class Device_4652 extends base.Base_Device {
    constructor(data, config_page) {
        super(data, config_page);

        this.dev_types = dev_types;
        switch (this.model_id) {
            case 2: this.nb_slots = 2; break;
        }
        this.setup_slots(data);        
        this.set_device_reference();
        this.setup_config_page();
    };
}