export class Slot_Select_Field {
    constructor() {
        // event stuff
        this._on_change = null;
        // private stuff
        this._label = this.create_label_element();
        this._select = this.create_select_element();
        this._field = this.create_field_element();
    };
    set on_change(func) {
        this._on_change = func;
    };
    create_label_element() {
        let el = document.createElement('label');
        el.classList.add('device-slot-label');
        return el;
    };
    set label(label) {
        this._label.textContent = label;
    };
    create_select_element() {
        let el = document.createElement('select');
        el.classList.add('device-slot-select');
        let field = this;
        el.addEventListener('change', event => {
            if (field._on_change!==null) {
                let val = el.value;
                field._on_change(val);
            }
        });
        return el;
    };
    append_option(value, text, selected) {
        var opt = new Option(text, value, false, selected);
        this._select.appendChild(opt);
    };
    create_field_element() {
        let el = document.createElement('div');
        el.classList.add('device-slot-line');
        el.appendChild(this._label);
        el.appendChild(this._select);
        return el;
    }
    get field() {
        return this._field;
    }
}

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
        console.log(name, field);
        if (this.fields[name]!==undefined);
        this.fields[name] = field;
        this.el_slot.appendChild(field.field)
    };
}