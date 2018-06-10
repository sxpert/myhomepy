export class Base_Slot_Model {
    constructor(data) {
        this._on_value_updated =null
        let options = data.options;
        if (options!==undefined) {
            this.kos = options.KO;
            this.lists = options.lists;
            this.conds = options.conds;
            this.fields = options.fields;
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
    get data() {
        return this.values;
    }
    update(data) {
        let keys = Object.keys(data.values);
        for(var k=0; k<keys.length; k++) {
            let key = keys[k];
            this.set_value(key, data.values[key]);
        }
    }
    generate_field_name(field) {
        var name = field.access+'_'+field.var_name;
        if (field.array_index!==null) name += '_'+field.array_index
        return name
    }
    get_field(field_name) {

    };
    get_value(name, array_index=null) {
        var v = undefined;
        if (this.values!==null)
            v = this.values[name]
        if (v===undefined) {
            // time to return some sensible default, depending on type, if possible
            if (this.fields!==null) {
                let f = this.fields[name];
                if (f!==undefined) {
                    let values = f.values
                    let type = values[0];
                    switch(type) {
                        case 'address': v = {a:0, pl:1}; break;
                        case 'area': v = 0; break;
                        case 'group': v = 1; break;
                        case 'int': v = values[1]; break;
                        case 'list': v = (values[1]!==null) ? values[1].values[0] : null; break;
                    }
                }
            }
        }
        return v;
    };
    set_value(name, value) {
        // we expect the value to be a string... make an int of it...
        if (typeof(value) === 'string')
            value = parseInt(value);
        // check the value
        var ok = false;
        if (this.fields!==null) {
            let f = this.fields[name];
            if (f!==undefined) {
                var type = f.values[0];
                switch(type) {
                    case 'address': 
                        console.log(type, value);
                        let not_0_0 = !((value.a==0)&&(value.pl==0));
                        let a_valid = ((value.a>=0)&&(value.a<=10));
                        let pl_valid = ((value.pl>=0)&&(value.pl<=15));
                        ok = not_0_0 && a_valid && pl_valid; 
                        break;
                    case 'area': ok = ((value.area>=0)&&(value.area<=10)); break;
                    case 'group': ok = ((value.group>=1)&&(value.group<=255)); break;
                    case 'int': ok = ((value>=f.values[1])&&(value<=f.values[2])); break;
                    case 'list':      
                        if (f.values[1] !== undefined) {
                            let values = f.values[1]
                            let options = values.values;
                            ok = options.indexOf(value)!=-1;
                        }
                        break;
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