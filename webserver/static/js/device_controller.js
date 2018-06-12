import * as ajax from './ajax.js';
import * as tree from './tree_control.js';
import * as bdm from './device_models/base_device_model_stub.js';
import * as dev_conf_view from './device_config_view.js';
import * as tabs_view from './tabs_view.js';
import * as slot_controller from './slot_controller.js';

export class Device {
    constructor(devices, data) {
        this.tree_item = null;
        this.devices = devices;
        this.id = data.id
        this.label = data.id;
        this.icon = data.icon;
        this.device_model = null;
        this.slot_controllers = null;
        this.config_view = null;
        this.tabs_view = null;
    };
    get_tree_item() { 
        if (this.tree_item === null) {
            var item = new tree.TreeItem(this.label, 'devices/'+this.icon);
            var device = this;
            item.on_click(function() {
                device.setup_config_view();
            });
            this.tree_item = item;
        }
        return this.tree_item;
    };
    setup_config_view() {
        if (this.device_model===null) {
            let dc = this;
            new bdm.Base_Device_Model_Stub(
                this.devices.system.system_id, this.id, 
                function (stub) {
                    dc.set_device_model(stub);
                });
        } else {
            // model is already there, time to setup the view
            if (this.config_view===null) {
                let controller = this;
                this.config_view = new dev_conf_view.Device_Config_View();
                this.config_view.device_icon = this.device_model.icon;
                this.config_view.manufacturer_logo = this.device_model.manufacturer_logo;
                this.config_view.device_reference = this.device_model.device_reference;
                this.config_view.name = this.device_model.name;
                this.config_view.on_name_change = function(new_name) {
                    controller.device_model.name = new_name;
                    controller.config_view.name = controller.device_model.name;
                }
                this.config_view.on_discover_request = function() {
                    controller.config_view.enabled = false;
                    controller.device_model.discover_device();
                }
                this.config_view.on_program_request = function() {
                    console.log('programming requested');
                    controller.config_view.enabled = false;
                    controller.device_model.program_device();
                }
                if (this.slot_controllers.length>1) {
                    // need a tab view
                    this.tabs_view = new tabs_view.Tabs_View();
                    this.config_view.tabs = this.tabs_view;
                }
                for(var i=0; i<this.slot_controllers.length; i++) {
                    let slot = this.slot_controllers[i];
                    let index = i;
                    if (this.tabs_view!==null)
                        this.tabs_view.add_tab(index, this.device_model.tab_label(index));
                    slot.onWidthChanged = function(new_width) {
                        controller.slot_width_changed(index, new_width);
                    }
                    this.config_view.set_slot(i, slot.element);
                }
            }
            this.config_view.show('main-content');
        }
    };
    slot_width_changed(slot_index, new_width) {
        if (this.tabs_view!=null)
            this.tabs_view.change_tab_width(slot_index, new_width);
    };
    set_device_model(stub) {
        let controller = this;
        if (stub.success) {
            this.device_model = stub.device_model;
            this.device_model.on_updated = function() {
                controller.update_view();
                controller.config_view.enabled = true;
            }
            // this.device_model.set_address_model()
            // create slot controllers
            let nb_slots = this.device_model.nb_slots
            this.slot_controllers = new Array(nb_slots);
            for(var i=0; i<nb_slots; i++) 
                this.slot_controllers[i] = new slot_controller.Slot_Controller(this.device_model.slots[i]);
            this.setup_config_view();
        } else 
            console.log('Unable to obtain device_model from server');
    };
    update_view() {
        console.log('updating view');
    }
}
