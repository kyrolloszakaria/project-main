# debugging tool
import inspect

def get_type_from_expression(exp):
        if exp.t.f.int:
            return "int"
        elif exp.t.f.float:
            return "float"
        elif exp.t.f.string:
            return "string"
        else:
            return "error"

def print_function_name(notes = ""):
    frame = inspect.currentframe()
    try:
        caller_name = inspect.getframeinfo(frame.f_back).function
        print("This program reached:", caller_name, f" {notes}")
    finally:
        del frame  # Make sure to clean up the frame

class Binding:
    pass

class IntBinding(Binding):
    def __init__(self, value):
        self.value = value

class FloatBinding(Binding):
    def __init__(self, value):
        self.value = value

class StringBinding(Binding):
    pass

class BoolBinding(Binding):
    pass

class ProcBinding(Binding):
    def __init__(self, params, return_type):
        self.params = params  # List of parameter types
        self.return_type = return_type  # Return type of the procedure

class SymbolTable:
    def __init__(self, parent=None):
        print_function_name("to create a new symbol table")
        self.parent = parent
        self.bindings = {}

    def bind(self, name, binding):
        print_function_name()
        if name in self.bindings:
            raise Exception(f"Symbol '{name}' already exists in this scope.")
        self.bindings[name] = binding

    def bind_proc(self, name, params, return_type):
        print_function_name()
        if name in self.bindings:
            raise Exception(f"Symbol '{name}' already exists in this scope.")
        self.bindings[name] = ProcBinding(params, return_type)

    def lookup(self, name):
        print_function_name()
        if name in self.bindings:
            return self.bindings[name]
        if not self.parent:
            raise Exception(f"Symbol '{name}' is undeclared.")
        return self.parent.lookup(name)

    def enter(self):
        print_function_name("to create a new scope")
        return SymbolTable(parent=self)

    def exit(self):
        print_function_name()
        if not self.parent:
            raise Exception("Cannot exit from the global scope.")
        return self.parent
