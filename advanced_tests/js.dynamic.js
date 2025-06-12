class DynamicObj {
    constructor() {
        // Dynamic property assignment
        this['field_' + Math.random()] = 42;
    }
    setField(name, value) {
        this[name] = value;
    }
}