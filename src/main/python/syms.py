# NOTE: This is the code from our in-class activity.
# Feel free to modify it as you see fit.


class Binding:
    pass


class IntBinding(Binding):
    pass


class FloatBinding(Binding):
    pass


class SymbolTable:
    def __init__(self, parent=None):
        self.parent = parent
        self.bindings = {}

    def bind(self, name, binding):
        if name in self.bindings:
            raise Exception("no")
        self.bindings[name] = binding

    def lookup(self, name):
        if name in self.bindings:
            return self.binings[name]
        if not self.parent:
            raise Exception("no")
        return self.parent.lookup(name)

    def enter(self):
        return SymbolTable(parent=self)

    def exit(self):
        if not self.parent:
            raise Exception("no")
        return self.parent
