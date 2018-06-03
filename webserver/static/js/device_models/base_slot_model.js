export class Base_Slot_Model {
    constructor(data) {
        this._on_value_updated =null
        let options = data.options;
        if (options!==undefined) {
            let fields = options.fields;
            if (fields!==undefined) {
                // turn the array unto a dict
                let dict = {};
                for(var f=0; f<fields.length; f++)
                    dict[fields[f].name] = fields[f];
                this.fields = fields;
                this.fields_dict = dict;
            } else    
                this.fields = null;
        } else
            this.fields = null;
        let values = data.values;
        if (values!==undefined) 
            this.values = data.values;
        else
            this.values = null;
    };
    set on_value_updated(func) {
        this._on_value_updated = func;
    }
    update(data) {
        let keys = Object.keys(data.values);
        for(var k=0; k<keys.length; k++) {
            let key = keys[k];
            this.set_value(key, data.values[key]);
        }
    }
    get_field(field_name) {

    };
    get_value(name) {
        var v = undefined;
        if (this.values!==null)
            v = this.values[name]
        if (v===undefined) {
            // time to return some sensible default, depending on type, if possible
            if (this.fields_dict!==null) {
                let f = this.fields_dict[name];
                if (f!==undefined) {
                    switch(f.type) {
                        case 'address': v = {a:0, pl:1}; break;
                        case 'area': v = 0; break;
                        case 'group': v = 1; break;
                        case 'integer': v = f.min; break;
                        case 'select': v = 0; break;
                    }
                }
            }
        }
        return v;
    };
    set_value(name, value) {
        // check the value
        var ok = false;
        if (this.fields_dict!==null) {
            let f = this.fields_dict[name];
            if (f!==undefined) {
                switch(f.type) {
                    case 'address': 
                        let not_0_0 = !((value.a==0)&&(value.pl==0));
                        let a_valid = ((value.a>=0)&&(value.a<=10));
                        let pl_valid = ((value.pl>=0)&&(value.pl<=15));
                        ok = not_0_0 && a_valid && pl_valid; 
                        break;
                    case 'area': ok = ((value.area>=0)&&(value.area<=10)); break;
                    case 'group': ok = ((value.group>=1)&&(value.group<=255)); break;
                    case 'integer': ok = ((value>=f.min)&&(value<=f.max)); break;
                    case 'select': ok = ((value>=0)&&(value<f.options.length)); break;
                    default:
                        console.log('Base_Slot_Model::set_value', name, value, 'ERROR')
                        console.log('unhandled field type', f);
                        ok = true;
                }
            }
        }
        if (ok) {
            this.values[name] = value;
            if (this._on_value_updated!==null)
                this._on_value_updated(name);
        }
        return ok;
    };
}