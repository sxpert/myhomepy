import * as slot_view from './slot_view.js';

export class Slot_Controller {
    constructor(slot_model) {
        console.log('Slot_Controller::constructor', slot_model);
        this.slot_model = slot_model;
        this.slot_view = new slot_view.Slot_View();
        this.initialize_view();
    };
    get element() {
        return this.slot_view.element;
    };
    initialize_view() {
        let model = this.slot_model;
        if (model.fields===null)
            return;

        console.log('model', model);
        let fields = model.fields;
        let dict = {};
        for(var f=0; f<fields.length; f++) {
            let field = fields[f];
            let order = field.order;
            if (dict[order]===undefined) 
                dict[order] = [];
            dict[order].push(field);
        }
        let keys = Object.keys(dict);
        for(var i=0; i<keys.length; i++) {
            let list = dict[keys[i]];
            for(var l=0; l<list.length; l++) {
                let field = list[l];
                var field_view = null;
                switch (field.type) {
                    case 'select': 
                        field_view = new slot_view.Slot_Select_Field();
                        let name = field.name;
                        let controller = this;
                        field_view.label = name;
                        field_view.on_change = function(value) {
                            controller.field_changed(name, value);
                        };
                        let options = field.options;
                        let current = model.get_value(field.name);
                        for(var o=0; o<options.length; o++)
                            field_view.append_option(o, options[o], o == current);
                        break;
                }
                if (field_view!==null)
                    this.slot_view.set_field(field.name, field_view);
            }
        }
    };
    field_changed(name, value) {
        console.log('Slot_Controller::field_changed', name, value);
    }
}