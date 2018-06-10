export class KO_View {
    constructor() {
        this.fields = null;
        this.ko_el = this.create_ko_element();
    };
    create_ko_element() {
        let el = document.createElement('div');
        el.classList.add('device-ko');
        return el;
    };
    get element() {
        return this.ko_el;
    }
    set_field(name, field) {
        if (this.fields===null)
            this.fields = {};
        if (this.fields[name]!==undefined);
        this.fields[name] = field;
        this.ko_el.appendChild(field.field)
    };
    set_visible(name, visible) {
        if (this.fields === null) return;
        let f = this.fields[name];
        if (f!==undefined)
            f.visible = visible;
    }
    set_field_valid(name) {
        console.log('value for field', name, 'was valid');
    };
    set_field_invalid(name) {
        console.log('value for field', name, 'was invalid');
    };
    set_value(name, value) {
        let field = this.fields[name];
        if (field!==undefined)
            field.value = value;
    }
}