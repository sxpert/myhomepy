import * as base from './base_device_model.js';

export class Device_4652 extends base.Base_Device_Model {
    constructor(data) {
        super(data);
    };
    tab_label(index) {
        return this._device_types[this.model_id].tab_labels[index];
    }
}

Device_4652.prototype._device_types = {
    2 : {
        tab_labels: ['Left Button', 'Right Button'],
        nb_slots : 2,
        references : {
            'BRAND_UNDEFINED' : {
                icon: 'unknown',
                0 : '4652/2'
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
};