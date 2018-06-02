export class Base_Slot_Field_View {
    constructor() {
        // event stuff
        this._on_change = null;
        // private stuff
        this._label = this.create_label_element();
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
    create_field_element() {
        let el = document.createElement('div');
        el.classList.add('device-slot-line');
        el.appendChild(this._label);
        return el;
    };
    get field() {
        return this._field;
    };
    set visible(visible) {
        // console.log('Base_Slot_Field_View::visible', this._label.textContent, visible);
        this._field.hidden = !visible;
    };
}