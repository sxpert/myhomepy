export class Base_Slot_Model {
    constructor(data) {
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
    get_field(field_name) {

    };
    get_value(name) {
        if (this.values===null)
            return undefined;
        let v = this.values[name]
        if (v===undefined)
            return undefined;
        return v;
    };
    set_value(name, value) {
        // check the value
        var ok = false;
        if (this.fields_dict!==null) {
            let f = this.fields_dict[name];
            if (f!==undefined) {
                switch(f.type) {
                    case 'select':
                        if ((value>=0)&&(value<f.options.length))
                            ok=true;
                        break;
                    default:
                        console.log('Base_Slot_Model::set_value', name, value, 'ERROR')
                        console.log('unhandled field type', f);
                        ok = true;
                }
            }
        }
        if (ok)
            this.values[name] = value;
        return ok;
    };
}