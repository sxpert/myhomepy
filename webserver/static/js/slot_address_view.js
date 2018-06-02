import * as slot_field from './base_slot_field_view.js';

export class Slot_Address_View extends slot_field.Base_Slot_Field_View {
    constructor() {
        super();
        let el = this._field;
        this._a_label = this.create_input_label_element('A');
        el.appendChild(this._a_label);
        this._a_input = this.create_input_element();
        el.appendChild(this._a_input);
        this._pl_label = this.create_input_label_element('PL');
        el.appendChild(this._pl_label);
        this._pl_input = this.create_input_element();
        el.appendChild(this._pl_input);
    };
    create_input_label_element(text) {
        let el = document.createElement('label');
        el.classList.add('device-slot-address-label');
        el.textContent = text;
        return el;
    };
    create_input_element() {
        let el = document.createElement('input');
        el.setAttribute('type', 'text');
        el.classList.add('device-slot-address');
        let field = this;
        el.addEventListener('change', event => {
            if (field._on_change!==null) {
                let val = el.value;
                field._on_change(val);
            }
        });
        return el;
    };
}
