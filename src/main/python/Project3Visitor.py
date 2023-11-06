from asts import AbstractVisitor
from syms import SymbolTable, ProcBinding, VarBinding


class Project3Visitor(AbstractVisitor):
    def __init__(self):
        self.current_scope = SymbolTable()  # Create the root symbol table
        self.current_type = None  # Track the current type in context

    def error(self, message):
        print(message)
        raise Exception(message)

    def visitProgram(self, node, arg: SymbolTable):
        try:
            node.b.accept(self, arg)
        except Exception as e:
            return str(e)

        return "OK"

    def visitBlock(self, node, arg: SymbolTable):
        try:
            self.current_scope = self.current_scope.enter()  # Enter a new scope

            # Visit variable declarations
            for decl in node.decls:
                decl.accept(self, arg)

            # Visit statements
            for stmt in node.stmts:
                stmt.accept(self, arg)
        except Exception as e:
            return str(e)
        finally:
            self.current_scope = self.current_scope.exit()  # Exit back to the original scope

    def visitVariableDeclaration(self, node, arg: SymbolTable):
        var_type = arg.lookup(node.type)
        if not var_type:
            self.error(f"Type '{node.type}' is not defined in variable declaration.")
        
        if node.rhs:
            expr_type = node.rhs.accept(self, arg)
            if var_type != expr_type:
                self.error(f"Cannot assign expression of type {expr_type} to a variable of type {var_type}.")

        self.current_scope.bind(node.id, VarBinding(var_type))  # Bind the variable to its type

    def visitProcedureDeclaration(self, node, arg: SymbolTable):
        proc_type = ProcBinding()
        self.current_scope.bind(node.id, proc_type)  # Bind the procedure

        try:
            self.current_scope = self.current_scope.enter()  # Enter a new scope

            # Visit formal parameters
            if node.params:
                params = node.params.accept(self, arg)
                for param_id, param_type in zip(params[::2], params[1::2]):
                    self.current_scope.bind(param_id, VarBinding(param_type))

            # Visit the block
            node.b.accept(self, arg)
        except Exception as e:
            return str(e)
        finally:
            self.current_scope = self.current_scope.exit()  # Exit back to the original scope

    def visitFormalParameters(self, node, arg: SymbolTable):
        params = []
        for i in range(0, len(node.params), 2):
            param_id = node.params[i]
            param_type = arg.lookup(node.params[i + 1])
            if not param_type:
                self.error(f"Type '{node.params[i + 1]}' is not defined.")
            params.extend([param_id, param_type])

        return params

    def visitStatement(self, node, arg: SymbolTable):
        try:
            if node.assign:
                node.assign.accept(self, arg)
            if node.call:
                node.call.accept(self, arg)
            if node.ret:
                node.ret.accept(self, arg)
            if node.ifs:
                node.ifs.accept(self, arg)
            if node.whiles:
                node.whiles.accept(self, arg)
        except Exception as e:
            raise e

    def visitAssignmentStatement(self, node, arg: SymbolTable):
        var_binding = arg.lookup(node.id)
        if not var_binding:
            self.error(f"'{node.id}' undeclared")
        
        expr_type = node.e.accept(self, arg)
        if var_binding.type != expr_type:
            self.error(f"Cannot assign expression of type {expr_type} to a variable of type {var_binding.type}.")

    def visitReturnStatement(self, node, arg: SymbolTable):
        return node.e.accept(self, arg)

    # Implement other visit methods for IfStatement, WhileStatement, Condition, Expression, Term, Factor, etc.
