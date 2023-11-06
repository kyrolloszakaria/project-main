class Binding:
    def __init__(self, name, type=None):
        self.name = name
        self.type = type  # Type of the binding

class SymbolTable:
    def __init__(self, parent=None):
        self.parent = parent
        self.bindings = {}

    def bind(self, name, binding):
        if name in self.bindings:
            raise Exception(f"Symbol '{name}' is already declared in this scope.")
        self.bindings[name] = binding

    def lookup(self, name):
        binding = self.bindings.get(name)
        if binding is not None:
            return binding
        if self.parent is not None:
            return self.parent.lookup(name)
        return None

    def enter(self):
        new_scope = SymbolTable()
        new_scope.parent = self  # Set the parent scope
        return new_scope

    def exit(self):
        return self.parent
