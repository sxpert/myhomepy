export class Base_Slot {
    //------------------------------------------------------------------------
    //
    // Major javascript object hacking
    //
    //
    set_behavior(field) {
        let slot=this;
        // add behavior for every type
        field.recurse_conditions = function(cond) {
            // step 1: identify op
            var op = cond.op;
            switch (op) {
                // should not happen, obviously
                case undefined: 
                    console.log('no \'op\' specified');    
                    return true;
                case '==': 
                    if (cond.field===undefined) {
                        console.log('no \'field\' specified');
                        return true;
                    }
                    var f = slot.get_value(cond.field);
                    if (cond.value===undefined) {
                        console.log('no \'value\' specified');
                        return true;
                    }
                    return (f==cond.value);
                case 'in':
                    if (cond.field===undefined) {
                        console.log('no \'field\' specified');
                        return true;
                    }
                    var f = slot.get_value(cond.field);
                    if (cond.values===undefined) {
                        console.log('no \'values\' specified');
                        return true;
                    }
                    if (!Array.isArray(cond.values)) {
                        console.log('\'values\' should be an array', cond.values);
                        return true;
                    }
                    // scan the array, find if f is one of the values,
                    // returns true when that happens 
                    // (no need to scan the rest of the array)
                    for(var i=0; i<cond.values.length; i++) { 
                        if (f==cond.values[i])
                            return true;
                    }
                    // scanning the array unsuccessful...
                    return false;
                case 'and':
                    if ((cond.conditions === undefined) || (! Array.isArray(cond.conditions))) {
                        console.log('there should be an array of conditions in \'conditions\'', cond);
                        return true;
                    }
                    var result = true;
                    for(var ic=0; ic<cond.conditions.length; ic++)
                        result &= this.recurse_conditions(cond.conditions[ic]);
                    return result;
                default:
                    console.log('unknown operator \''+op+'\'', cond);
            }
            return true;
        };
        field.show_test = function(){
            // tests if the control should be displayed
            // if display is not defined, the thing should always be visible
            if (this.display===undefined)
                return true;
            // this gets more complicated ;)
            if (this.display.conditions!==undefined)
                return this.recurse_conditions(this.display.conditions);
            return false;
        };
    }
}
