import * as slot_view from './slot_view.js';
import * as address_view from './slot_address_view.js';
import * as area_view from './slot_area_view.js';
import * as group_view from './slot_group_view.js';
import * as integer_view from './slot_integer_view.js';
import * as select_view from './slot_select_view.js';

export class Slot_Controller {
    constructor(slot_model) {
        this.slot_model = slot_model;
        let controller = this;
        slot_model.on_value_updated = function(name) {
            controller.value_updated(name);
        };
        this.slot_view = new slot_view.Slot_View();
        this.initialize_view();
        this.set_fields_visibility();
    };
    get element() {
        return this.slot_view.element;
    };
    initialize_view() {
        let model = this.slot_model;
        if (model.fields===null)
            return;
        let names = model.names;
        let fields = model.fields;
        let display_order = {};
        for(var f=0; f<names.length; f++) {
            let field = fields[names[f]];
            let order = field.disp.order;
            if (display_order[order]===undefined) 
                display_order[order] = [];
            display_order[order].push(field);
        }
        let display_order_list = Object.keys(display_order)
        for(var i=0; i<display_order_list.length; i++) {
            let field_list = display_order[display_order_list[i]];
            for(var l=0; l<field_list.length; l++) {
                var field_view = null;
                let controller = this;
                // field related variables
                let field = field_list[l];
                let name = field.name;                
                let values = field.values;
                var type = values[0];
                // values and variables
                let current = model.get_value(name);
                var options = null;
                switch (type) {
                    case 'address':
                        field_view = new address_view.Slot_Address_View();
                        field_view.label = field.disp.label;
                        field_view.on_change = function(value) {
                            controller.field_changed(name, value);
                        }
                        field_view.value = current;
                        break;
                    case 'area': 
                        options = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10];
                        field_view = new area_view.Slot_Area_View();
                        field_view.label = field.disp.label;
                        field_view.on_change = function(value) {
                            controller.field_changed(name, value);
                        };
                        for(var o=0; o<options.length; o++)
                            field_view.append_option(o, options[o], o == current);
                        break;
                    case 'group':
                        field_view = new group_view.Slot_Group_View();
                        field_view.label = field.disp.label;
                        field_view.on_change = function(value) {
                            controller.field_changed(name, value);
                        };
                        field_view.value = current;
                        break;
                    case 'int':
                        field_view = new integer_view.Slot_Integer_View();
                        field_view.label = field.disp.label;
                        field_view.on_change = function(value) {
                            controller.field_changed(name, value);
                        };
                        field_view.value = current;
                        break;
                    case 'list':
                        field_view = new select_view.Slot_Select_View();
                        field_view.label = field.disp.label;
                        field_view.on_change = function(value) {
                            controller.field_changed(name, value);
                        };
                        if ((values[1] !== undefined) && (values[1] !== null)) {
                            options = values[1].values;
                            var opt_names = values[1].names;
                            for(var o=0; o<options.length; o++)
                                field_view.append_option(options[o], opt_names[o], options[o] == current);
                        }
                        break;
                    default:
                        console.log('unknown type', field.name, field.type);
                }
                if (field_view!==null)
                    this.slot_view.set_field(field.name, field_view);
            }
        }
    };
    recurse_conditions(cond) {
        // step 1: identify op
        var op = cond[0];
        switch (op) {
            // should not happen, obviously
            case undefined: 
                console.log('no \'op\' specified');    
                return true;
            case '==': 
                var field = cond[1];
                var value = cond[2];
                if (field===undefined) {
                    console.log('no \'field\' specified');
                    return true;
                }
                var f = this.slot_model.get_value(field);
                if (value===undefined) {
                    console.log('no \'value\' specified');
                    return true;
                }
                return (f==value);
            case 'in':
                var field = cond[1];
                var values = cond[2];
                if (field===undefined) {
                    console.log('no \'field\' specified');
                    return true;
                }
                var f = this.slot_model.get_value(field);
                if (values===undefined) {
                    console.log('no \'values\' specified');
                    return true;
                }
                if (!Array.isArray(values)) {
                    console.log('\'values\' should be an array', values);
                    return true;
                }
                if (values.indexOf(f) != -1)
                    return true;
                return false;
            case 'and':
                var conditions = cond[1]
                if ((conditions === undefined) || (! Array.isArray(conditions))) {
                    console.log('there should be an array of conditions in \'conditions\'', cond);
                    return true;
                }
                var result = true;
                for(var ic=0; ic<conditions.length; ic++)
                    result = result && this.recurse_conditions(conditions[ic]);
                return result;
            default:
                console.log('unknown operator \''+op+'\'', cond);
        }
        return true;
    };
    set_fields_visibility(){
        let fields = this.slot_model.fields;
        let field_names = Object.keys(fields);
        for(var f=0; f<field_names.length; f++) {
            var field_name = field_names[f];
            let field = fields[field_name];
            var can_display = true;
            if (field.cond!==undefined)
                can_display = this.recurse_conditions(field.cond);
            this.slot_view.set_visible(field_name, can_display);
        }   
    };
    field_changed(name, value) {
        if (this.slot_model.set_value(name, value)) 
            this.slot_view.set_field_valid(name);
        else  
            this.slot_view.set_field_invalid(name);
        this.set_fields_visibility();
    };
    value_updated(name) {
        var value = this.slot_model.get_value(name)
        this.slot_view.set_value(name, value);
        this.set_fields_visibility();
    }
}