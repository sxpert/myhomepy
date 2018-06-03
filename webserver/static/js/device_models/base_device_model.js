import * as ajax from '../ajax.js';
import * as base_slot_model from './base_slot_model.js';

export class Base_Device_Model {
    constructor(data) {
        // event related stuff
        this._system_id = null;
        this._on_updated = null;
        // status
        this.changed = false;
        // these are not updatable
        this.id = data.id;
        this.subsystem = data.subsystem;
        this.model_id = data.model_id;
        this._icon = 'device';
        // these may be updatable
        this.brand_id = data.brand_id;
        this.product_line = data.product_line;
        // this is user set
        this._name = data.name;
        this.description = data.description;
        this.slots = this.create_slots(data);
    };
    create_slots(data) {
        let slot_data = data.slots;
        if (slot_data===undefined) {
            console.log('no slot data in', data);
            return null;
        }
        if (this._device_types===undefined) {
            console.log('no _device_types in', this);
            return null;
        }
        let device_model = this._device_types[this.model_id];
        if (device_model.nb_slots===undefined) {
            console.log('no nb_slots in', device_model);
            return null;
        }
        let nb_slots = device_model.nb_slots;
        var slot_class = base_slot_model.Base_Slot_Model;
        if (device_model.slot_class!==undefined) {
            slot_class = device_model.slot_class;
            console.log('found slot_class', slot_class);
        }
        var slots = new Array(nb_slots);
        for(var i=0; i<nb_slots; i++) 
            slots[i] = new slot_class(slot_data[i]);
        return slots;
    }
    /*************************************************************************
     * 
     * methods to call in the web api for refreshing data in the model 
     * 
     */
    set system_id(system_id) {
        this._system_id = system_id
    }
    discover_device() {
        if ((this._system_id===undefined)||(this._system_id === null)) return false;
        var url = '/api/do-device-discovery?system_id='+this._system_id+'&device_id='+this.id;
        var model = this;
        ajax.get_json(url,
            function(data) {
                if (data.ok !== undefined && data.ok === true) {
                    data = data.device;
                    if (data!==undefined) 
                        return model.update(data);
                    console.log('problem, no \'device\' in ', data);
                }
            },
            function(request){
                console.log('error', request);
            }
        );                
    }
    update(data) {
        console.log('update the model with data', data);
        // update the device too...

        // normally only the slots should be modified
        for(var s=0; s<this.slots.length; s++) {
            this.slots[s].update(data.slots[s]);
        }
        if (this._on_updated!==null) 
            this._on_updated();
    }
    set on_updated(func) {
        this._on_updated = func;
    }
    /*************************************************************************
     * 
     * model properties
     * 
     */
    get icon() {
        return 'devices/'+this._icon;
    };
    get manufacturer_logo() {
        let manuf_logo_pfx = 'manufacturers/';
        var brand_icon = undefined;
        if (this._device_types!==undefined) {
            let device_model = this._device_types[this.model_id];
            if (device_model!==undefined) {
                let references = device_model.references;
                if (references!==undefined) {
                    let brand_info = references[this.brand_id];
                    if (brand_info!==undefined) {
                        brand_icon = brand_info.icon;
                    }
                }
            }
        }
        if (brand_icon!==undefined) 
            return manuf_logo_pfx+brand_icon;
        return manuf_logo_pfx+'unknown';
    };
    get device_reference() {
        var reference = undefined;
        if (this._device_types!==undefined) {
            let device_model = this._device_types[this.model_id];
            if (device_model!==undefined) {
                let references = device_model.references;
                if (references!==undefined) {
                    let brand_info = references[this.brand_id];
                    if (brand_info!==undefined) {
                        reference = brand_info[this.product_line];
                    }
                }
            }
        }
        if (reference===undefined) 
            return '<unknown>';
        return reference;
    };
    get name() {
        if ((this._name === undefined) || (this._name.length == 0))
            return this.id;
        return this._name;
    };
    set name(new_name) {
        if (this._name!=new_name) {
            this.changed = true;
            this._name = new_name;
        }
    }
    get nb_slots() {
        if (this.slots!==null)
            return this.slots.length;
        return 0;
    }
}