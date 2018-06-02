import * as slot_field from './base_slot_field_view.js';

export class Slot_Integer_View extends slot_field.Base_Slot_Field_View {
    constructor() {
        super();
        this._input = this.create_input_element();
        this._field.appendChild(this._input);
    };
    create_input_element() {
        let el = document.createElement('input');
        el.setAttribute('type', 'text');
        el.classList.add('device-slot-integer');
        let field = this;
        el.addEventListener('change', event => {
            if (field._on_change!==null) {
                let val = el.value;
                field._on_change(val);
            }
        });
        return el;
    };
    set value(value) {
        console.log(this._label.textContent, 'setting value', value);
        this._input.value = value;
    }
}
