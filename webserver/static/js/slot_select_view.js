import * as slot_field from './base_slot_field_view.js';

export class Slot_Select_View extends slot_field.Base_Slot_Field_View {
    constructor() {
        super();
        this._select = this.create_select_element();
        this._field.appendChild(this._select);
    };
    create_select_element() {
        let el = document.createElement('select');
        el.classList.add('device-slot-select');
        let field = this;
        el.addEventListener('change', event => {
            if (field._on_change!==null) {
                let val = el.value;
                field._value_changed(val);
            }
        });
        return el;
    };
    append_option(value, text, selected) {
        var opt = new Option(text, value, false, selected);
        this._select.appendChild(opt);
    };
    set value(value) {
        this._select.value = value;
    }
}
