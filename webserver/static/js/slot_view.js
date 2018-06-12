export class Slot_View {
    constructor() {
        this._hidden = false;
        this.ko_el = null;
        this.ko_view = null;
        this.el_slot = this.create_slot_element();
    };
    create_slot_element() {
        let el = document.createElement('div');
        el.classList.add('device-slot');
        return el;
    };
    refresh_children() {
        if (this.el_slot===undefined) return;
        // should make this smarter...
        this.el_slot.innerHTML="";
        if (this.ko_el!==null) this.el_slot.appendChild(this.ko_el.field);
        if (this.ko_view!==null) this.el_slot.appendChild(this.ko_view.element);
    };
    set hidden(value) {
        this.el_slot.hidden = value;
        console.log(this.el_slot);
    }
    get element() {
        return this.el_slot;
    };
    set_ko_element(ko_el) {
        this.ko_el = ko_el;
        this.refresh_children();
    };
    set_ko_view(ko_view) {
        this.ko_view = ko_view;
        this.refresh_children();
    }
    set_visible(name, visible) {
        if (this.ko_view === null) return;
        this.ko_view.set_visible(name, visible);
    }
    set_field_valid(name) {
        console.log('value for field', name, 'was valid');
    };
    set_field_invalid(name) {
        console.log('value for field', name, 'was invalid');
    };
    set_value(name, value) {
        if (this.ko_view === null) return;
        this.ko_view.set_value(name, value);
    }
}