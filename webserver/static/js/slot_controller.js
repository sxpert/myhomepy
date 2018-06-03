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
                var options = null;
                let current = model.get_value(field.name);
                let name = field.name;
                let controller = this;
                switch (field.type) {
                    case 'address':
                        field_view = new address_view.Slot_Address_View();
                        field_view.label = name;
                        field_view.on_change = function(value) {
                            controller.field_changed(name, value);
                        }
                        field_view.value = current;
                        break;
                    case 'area': 
                        options = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10];
                        field_view = new area_view.Slot_Area_View();
                        field_view.label = name;
                        field_view.on_change = function(value) {
                            controller.field_changed(name, value);
                        };
                        for(var o=0; o<options.length; o++)
                            field_view.append_option(o, options[o], o == current);
                        break;
                    case 'group':
                        field_view = new group_view.Slot_Group_View();
                        field_view.label = name;
                        field_view.on_change = function(value) {
                            controller.field_changed(name, value);
                        };
                        field_view.value = current;
                        break;
                    case 'integer':
                        field_view = new integer_view.Slot_Integer_View();
                        field_view.label = name;
                        field_view.on_change = function(value) {
                            controller.field_changed(name, value);
                        };
                        field_view.value = current;
                        break;
                    case 'select':
                        options = field.options;
                        field_view = new select_view.Slot_Select_View();
                        field_view.label = name;
                        field_view.on_change = function(value) {
                            controller.field_changed(name, value);
                        };
                        for(var o=0; o<options.length; o++)
                            field_view.append_option(o, options[o], o == current);
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
        var op = cond.op;
        switch (op) {
            // should not happen, obviously
            case undefined: 
                console.log('no \'op\' specified');    
                return true;
            case '==': 
                if (cond.field===undefined) {
                    console.log('no \'field\' specified');
                    return true;
                }
                var f = this.slot_model.get_value(cond.field);
                if (cond.value===undefined) {
                    console.log('no \'value\' specified');
                    return true;
                }
                // console.log(cond.value, '==', cond.field, f, this.slot_model.values);
                return (f==cond.value);
            case 'in':
                if (cond.field===undefined) {
                    console.log('no \'field\' specified');
                    return true;
                }
                var f = this.slot_model.get_value(cond.field);
                if (cond.values===undefined) {
                    console.log('no \'values\' specified');
                    return true;
                }
                if (!Array.isArray(cond.values)) {
                    console.log('\'values\' should be an array', cond.values);
                    return true;
                }
                // scan the array, find if f is one of the values,
                // returns true when that happens 
                // (no need to scan the rest of the array)
                for(var i=0; i<cond.values.length; i++) { 
                    if (f==cond.values[i])
                        return true;
                }
                // scanning the array unsuccessful...
                return false;
            case 'and':
                if ((cond.conditions === undefined) || (! Array.isArray(cond.conditions))) {
                    console.log('there should be an array of conditions in \'conditions\'', cond);
                    return true;
                }
                var result = true;
                for(var ic=0; ic<cond.conditions.length; ic++)
                    result = result && this.recurse_conditions(cond.conditions[ic]);
                return result;
            default:
                console.log('unknown operator \''+op+'\'', cond);
        }
        return true;
    };
    set_fields_visibility(){
        let fields = this.slot_model.fields;
        for(var f=0; f<fields.length; f++) {
            let field = fields[f];
            var can_display = true;
            if (field.display!==undefined) {
                let display = field.display;
                if (display.conditions!==undefined)
                    // console.log(display.conditions);
                    can_display = this.recurse_conditions(display.conditions);
            }
            this.slot_view.set_visible(field.name, can_display);
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