import * as base from './base_device_model.js';

export class Device_F411 extends base.Base_Device_Model {
    constructor(data) {
        super(data)
    };
}

Device_F411.prototype._device_types = {
    129 : {
        nb_slots : 2,
        references : {
            'BRAND_UNDEFINED' : {
                icon: 'unknown',
                0 : 'F411/2'
            }
        }
    },
    130 : {
        nb_slots : 4,
        references : {
            'BRAND_UNDEFINED' : {
                icon: 'unknown',
                0 : 'F411/4'
            }
        }
    }
};