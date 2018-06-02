import * as base from './base_device_model.js';

export class Device_4652 extends base.Base_Device_Model {
    constructor(data) {
        super(data);
    };
}

Device_4652.prototype._device_types = {
    2 : {
        nb_slots : 2,
        references : {
            'BRAND_UNDEFINED' : {
                icon: 'unknown-1',
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
};