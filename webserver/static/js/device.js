import * as ajax from './ajax.js';
import * as tree from './tree_control.js';
import * as dev_config from './device_config_page.js';
import * as dev_4652 from './devices/4652.js';
import * as dev_F411 from './devices/F411.js';

let device_types = {
    'LIGHTING' : {
        2: dev_4652.Device_4652,
        129: dev_F411.Device_F411,
        130: dev_F411.Device_F411,
    }
}

export class Device {
    constructor(devices, data) {
        this.tree_item = null;
        this.config_page = null;
        this.devices = devices;
        this.id = data.id
        this.label = data.id;
        this.icon = data.icon;
        this.device = null;
    };
    get_tree_item() {
        if (this.tree_item === null) {
            var item = new tree.TreeItem(this.label, this.icon);
            var device = this;
            var click_func = function() {
                device.click();
            }
            item.on_click(click_func);
            this.tree_item = item;
        }
        return this.tree_item;
    };
    click() {
        console.log(this.label, 'clicked')
        var device = this;
        var url = '/api/get-device-data?system_id='+
            this.devices.system.system_id+
            '&device_id='+
            this.id;
        console.log(url);
        ajax.get_json(url,
            function(data) {
                if (data.ok !== undefined && data.ok === true) {
                    console.log('success', data);
                    data = data.device;
                    if (data!==undefined)
                        return device.setup_config_page(data);
                    console.log('problem, no \'device\' in ', data);
                }
            },
            function(request){
                console.log('error', request);
            }
        );
    };
    setup_config_page(data) {
        if ((data.subsystem===undefined)||(data.model_id===undefined))
            return console.log('missing either subsystem or model_id', data);
        let subsystem = device_types[data.subsystem];
        if (subsystem===undefined)
            return console.log('unable to find subsystem \''+data.subsystem+'\'');
        let device_class = subsystem[data.model_id];
        console.log(device_class);
        if (device_class===undefined)
            return console.log('unable to find config page for model '+dev.subsystem+'.'+dev.model_id);
        if (this.config_page===null)
            this.config_page = new dev_config.Device_Config_Page('main-content');
        data.icon = this.icon;
        data.id = this.id;
        this.device = new device_class(data, this.config_page);
    };
}
