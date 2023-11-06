class Binding:
    def __init__(self, name, symbol_type):
        self.name = name
        self.symbol_type = symbol_type


class IntBinding(Binding):
    pass

class FloatBinding(Binding):
    pass

class VarBinding(Binding):
    def __init__(self, name, vtype):
        super().__init__(name, "var")
        self.var_type = vtype

class ProcBinding(Binding):
    def __init__(self, name, params=None, return_type=None):
        super().__init__(name, "proc")
        self.params = params  # List of parameter types
        self.return_type = return_type  # Return type of the procedure

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
