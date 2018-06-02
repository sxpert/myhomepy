export class Base_Slot_Model {
    constructor(data) {
        let options = data.options;
        if (options!==undefined) {
            let fields = options.fields;
            if (fields!==undefined) 
                this.fields = options.fields;
            else    
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

    };
    set_value(name, value) {

    };
}