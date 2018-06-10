export class Base_Slot_Model {
    constructor(data) {
        this._on_value_updated =null
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
            for(var i_ko=0; i_ko<this.kos.ids.length; i_ko++) {
                let ko_names = []
                let ko_id = this.kos.ids[i_ko]
                let fields = this.fields[ko_id]
                for(var f=0; f<fields.length; f++){
                    ko_names[f] = this.generate_field_name(fields[f]);
                }
                this.names[ko_id] = ko_names;
            }
        }
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
    get_value(name) {
        if (name=='KO') {
            // special case !
            return this.values.KO;
        }
        //console.log('get_value', name);
        var v = undefined;
        let ko_name = this.values.KO;
        let names = this.names[ko_name];
        let index = names.indexOf(name);
        if (index>=0) {
            let field = this.fields[ko_name][index];
            let var_name = field.var_name;
            let v = this.values[var_name]
            let access = field.access;
            if (access=='array') {
                if (v!==null) v = v[field.array_index];
                if (v===null) v = undefined;
            }
            let field_type = field.field_type;
            switch (field_type) {
                case 'LIST': 
                    let list = this.lists[field.field_type_detail];
                    index = list.ids.indexOf(v);
                    if (index>=0) v = list.values[index];
                    else v = undefined;
                    break;
            }
            return v;
        } else {
            console.log('Base_Slot_Model.get_value : unable to find name', name);
            console.log(ko_name, names, index)
        }
        return undefined;

        //                 case 'address': v = {a:0, pl:1}; break;
        //                 case 'area': v = 0; break;
        //                 case 'group': v = 1; break;
        //                 case 'int': v = values[1]; break;
        //                 case 'list': v = (values[1]!==null) ? values[1].values[0] : null; break;
    };
    set_value(name, value) {
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
                default:
                    console.log('Base_Slot_Model::set_value', name, value, 'ERROR')
                    console.log('unhandled field type', f);
                    ok = true;
            }
            if (ok) {
                console.log('Base_Slot_Model.set_value', 'old value', this.values[var_name], 'new value', value);
                this.values[var_name] = value;
                if (this._on_value_updated!==null)
                    this._on_value_updated(name);
            }
            return ok;
        } else {
            console.log('Base_Slot_Model.set_value : unable to find name', name);
            console.log(ko_name, names, index)
        }
        return false;
    };
}