import * as ajax from '../ajax.js';
import * as dev_4652 from './4652.js';
import * as dev_4672m2 from './4672m2.js';
import * as dev_F411 from './F411.js';
import * as dev_4693 from './4693.js';


export class Base_Device_Model_Stub {
    constructor(system_id, id, callback) {
        this.system_id = system_id;
        this.callback = callback;
        this.success = false;
        this.device_model = null;
        var url = '/api/get-device-data?system_id='+system_id+'&device_id='+id;
        var bdms = this;
        ajax.get_json(url,
            function(data) {
                if (data.ok !== undefined && data.ok === true) {
                    data = data.device;
                    if (data!==undefined) 
                        return bdms.set_device_model(data);
                    console.log('problem, no \'device\' in ', data);
                }
            },
            function(request){
                console.log('error', request);
            }
        );        
    }
    set_device_model(data) {
        if ((data.subsystem===undefined)||(data.model_id===undefined))
            return console.log('missing either subsystem or model_id', data);
        let subsystem = this.device_types[data.subsystem];
        if (subsystem===undefined)
            return console.log('unable to find subsystem \''+data.subsystem+'\'');
        let device_class = subsystem[data.model_id];
        if (device_class===undefined)
            return console.log('unable to find config page for model '+data.subsystem+'.'+data.model_id);
        this.device_model = new device_class(data);
        this.device_model.system_id = this.system_id;
        this.success = true;
        this.callback(this);
    };
}

Base_Device_Model_Stub.prototype.device_types = {
    'LIGHTING' : {
        2: dev_4652.Device_4652,
        82: dev_4672m2.Device_4672M2,
        129: dev_F411.Device_F411,
        130: dev_F411.Device_F411,
    },
    'TEMP_CONTROL' : {
        21: dev_4693.Device_4693,
    }
};
