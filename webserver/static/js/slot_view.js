export class Slot_View {
    constructor() {
        this.fields = null;
        this.el_slot = this.create_slot_element();
    };
    create_slot_element() {
        let el = document.createElement('div');
        el.classList.add('device-slot');
        return el;
    };
    get element() {
        return this.el_slot;
    }
    set_field(name, field) {
        if (this.fields===null)
            this.fields = {};
        if (this.fields[name]!==undefined);
        this.fields[name] = field;
        this.el_slot.appendChild(field.field)
    };
    set_visible(name, visible) {
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