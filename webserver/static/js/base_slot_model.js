export class Base_Slot_Model {
    constructor(data) {
        this._on_value_updated =null

        let values = data.values;
        if (values!==undefined) 
            this.values = values;
        else
            this.values = {};

        let options = data.options;
        if (options!==undefined) {
            this.conds = options.conds;
            this.fields = options.fields;
            this.integers = options.integers;
            this.kos = options.kos;
            this.lists = options.lists;
        } else
            this.fields = null;
        // generate all field names
        this.names = {};
        if (this.fields!==null) {
            for(let ko_id of this.kos.ids) {  
                let ko_names = []
                let fields = this.fields[ko_id]
                for(let field of fields) {
                    ko_names.push(this.generate_field_name(field));
                    // add nonexistent values
                    var v = this.values[field.var_name];
                    // generate default
                    var default_value = field.default_value;
                    if(v===undefined) {
                        if (field.access=='array') v = [];
                        else v = default_value;
                    }
                    if ((Array.isArray(v))&&(field.access=='array')) {
                        if (v[field.array_index]===undefined) v[field.array_index]=default_value;
                    }
                    this.values[field.var_name] = v;
                }
                this.names[ko_id] = ko_names;
            }
        }
    };
    set on_value_updated(func) {
        this._on_value_updated = func;
    }
    get data() {
        return this.values;
    }
    update(data) {
        for(let key in data.values) {
            this.set_value(key, data.values[key]);
        }
    }
    generate_field_name(field) {
        var name = field.access+'_'+field.var_name;
        if (field.array_index!==null) name += '_'+field.array_index
        return name
    }
    get_symbolic_value_for_field(field) {
        if (field===undefined) return undefined;
        let var_name = field.var_name;
        let v = this.values[var_name];
        let access = field.access;
        if (access=='array') {
            if ((v!==undefined)&&(v!==null)) v = v[field.array_index];
            if (v===null) v = undefined;
        }
        if((v===null)||(v===undefined)) {
            v = field.default_value
            if ((v===null)&&(field.field_type=='LIST')) {
                let list = this.lists[field.field_type_detail]
                v = list.ids[0];
            }
        }
        return v;
    }
    get_value_for_field(field) {
       var v = this.get_symbolic_value_for_field(field);
        let field_type = field.field_type;
        switch (field_type) {
            case 'LIST': 
                let list = this.lists[field.field_type_detail];
                let index = list.ids.indexOf(v);
                if (index>=0) v = list.values[index];
                else v = undefined;
                break;
        }
        return v;
    };
    get_names() {
        // returns all field names for the current KO
        let ko_name = this.values.KO;
        let names = this.names[ko_name];
        return names;
    }
    get_field(name) {
        let ko_name = this.values.KO;
        let names = this.names[ko_name];
        let index = names.indexOf(name);
        if (index>=0) {
            return this.fields[ko_name][index];
        } else {
            // find if this name exist in other kos
            for(var ko_id in this.names) {
                let index = this.names[ko_id].indexOf(name);
                if (index>=0)
                    return this.fields[ko_id][index];
            }
            // find the field with this variable name in the ko
            for(var field of this.fields[ko_name]){
                if (field.var_name == name) {
                    // there may be something about arrays to be done, but not now
                    return field;
                }
            }
        }
        return undefined;
    };
    get_value(name) {
        if (name=='KO') {
            // special case !
            return this.values.KO;
        }
        let field = this.get_field(name);
        return this.get_value_for_field(field);
    };
    set_value(name, value) {
        if (name=='KO') {
            // special case
            this.values.KO = value;
            return true;
        }
        // we expect the value to be a string... make an int of it...
        let ko_name = this.values.KO;
        let names = this.names[ko_name];
        let index = names.indexOf(name);
        if (index>=0) {
            let field = this.fields[ko_name][index];
            let var_name = field.var_name;
            // check validity
            var ok = false;
            switch(field.field_type) {
                case 'BOOL': if ((value===true)||(value===false)) ok=true; break;
                case 'INTEGER':
                    value = parseInt(value);
                    if (value===NaN) value=undefined;
                    let int = this.integers[field.field_type_detail]
                    if (int!==undefined) ok = (value>=int.min)&&(value<=int.max);
                    else ok = true;
                    break;
                case 'LIST':
                    // value is a string damnint
                    value = parseInt(value);
                    let list = this.lists[field.field_type_detail];
                    let values = list.values;
                    let index = values.indexOf(value);
                    ok = index >= 0;
                    value = ok?list.ids[index]:value;
                    break;
                case 'TEMP': 
                    value = parseFloat(value); 
                    if (isNaN(value)) value=undefined;
                    else {
                        switch(field.field_type_detail) {
                            case 'temp_*_2': value = Math.round(value*2)/2; break;
                        }
                    }
                    ok = true;
                    break;
                default:
                    console.log('Base_Slot_Model::set_value', name, value, 'ERROR')
                    console.log('unhandled field type', f);
                    ok = true;
            }
            if (ok) {
                console.log('Base_Slot_Model.set_value', 'old value', this.values[var_name], 'new value', value);
                if (field.access=='array') {
                    console.log('setting array value for ', var_name, field.array_index, value);
                    var v = this.values[var_name];
                    if (v===undefined) {
                        // should create an array with the right dimension
                        v = [];
                    }
                    v[field.array_index] = value;
                    this.values[var_name] = v
                } else this.values[var_name] = value;
                if (this._on_value_updated!==null)
                    this._on_value_updated(name);
            }
                return ok;
        }
        return false;
    };
}