from asts import *
from syms import *

# debugging tool
import inspect

def print_function_name():
    frame = inspect.currentframe()
    try:
        caller_name = inspect.getframeinfo(frame.f_back).function
        print("This program reached:", caller_name)
    finally:
        del frame  # Make sure to clean up the frame

class Project3Visitor(AbstractVisitor):
    def getname(self, name, symbol_table):
        print_function_name()
        try:
            binding = symbol_table.lookup(name)
            if isinstance(binding, IntBinding):
                return 'int'
            elif isinstance(binding, FloatBinding):
                return 'float'
            elif isinstance(binding, StringBinding):
                return 'string'
            elif isinstance(binding, BoolBinding):
                return 'bool'
            elif isinstance(binding, ProcBinding):
                return 'proc'
            else:
                return f'error'  # Handle undeclared or unknown types
        except Exception as e:
            return 'error'  # Handle undeclared or unknown types

    def visitProgram(self, node, symbol_table):
        print_function_name()
        # Create a new symbol table for the program scope
        program_table = SymbolTable(parent=symbol_table)

        # Visit the block with the new symbol table
        if node.b:
            return node.b.accept(self, program_table)
        else:
            return 'OK'  # Return 'OK' if there's no block
        
    def visitBlock(self, node, symbol_table):
        print_function_name()
        # Create a new symbol table for the block scope
        block_table = symbol_table.enter()

        # Collect function types
        function_types = []

        # Visit variable declarations, procedure declarations, and statements
        if node.decls:
            for decl in node.decls:
                result = decl.accept(self, block_table) # variable declaration
                print(f"reulst: {result}")
                if result != 'OK':
                    return result  # Propagate error messages
                if isinstance(decl, ProcedureDeclaration):
                    # If it's a procedure declaration, collect its type
                    function_types.append('proc')

        if node.stmts:
            for stmt in node.stmts:
                result = stmt.accept(self, block_table)
                if result != 'OK':
                    return result  # Propagate error messages

        # Exit back to the original scope
        symbol_table.exit()

        # Return the type of the last thing checked
        if function_types:
            return function_types[-1]
        else:
            return 'OK'  # Return 'OK' if no functions were found

    def visitVariableDeclaration(self, node, symbol_table):
        print_function_name()
        # Look up ID1 in the current scope
        print("node.id: ", node.id)
        print("symbol_table of the block bindings:", symbol_table.bindings)
        if node.id in symbol_table.bindings:
            return f"Error: {node.id} already exists in this scope."

        # Get the type of the expression (right-hand side)
        print("rhs of expr: ", str(node.rhs))           #PROBLEM: what is the rhs value?
        expr_type = node.rhs.accept(self, symbol_table)
        print("expr_type: ", expr_type)

        # If ID2 is specified, make sure it matches the type of the expression
        print("ID2: (node.type): ", node.type)
        if node.type:
            print("ID2 is specified")
            declared_type = self.getname(node.type, symbol_table)
            if declared_type != expr_type:
                return f"Error: Cannot assign an expression of type '{expr_type}' to a variable of type '{declared_type}'."

        # Bind the variable to its type
        # Create an IntBinding or FloatBinding as appropriate
        print("before symbol_table.bind()")
        if expr_type == 'float':
            symbol_table.bind(node.id, FloatBinding(value=0.0))
        else:
            symbol_table.bind(node.id, IntBinding(value=0))
        print("Symbol table in variable declaration: ",symbol_table.bindings)

        # Return "OK" to indicate a valid variable declaration
        return "OK"

    def visitProcedureDeclaration(self, node, symbol_table):
        # Enter a new scope for the procedure
        print_function_name()
        proc_table = symbol_table.enter()

        # Ensure the name ID1 is not a type name
        if node.id in ["int", "float", "void", "string", "bool"]:
            raise Exception(f"Cannot use reserved name '{node.id}' for a procedure.")

        # Get the list of parameter types and bind parameter names to their types
        param_names = node.params.accept(self, proc_table)
        print("proc_table bindings: ", proc_table.bindings)
        # Get the return type from ID2 or use 'void' if none is given
        return_type = self.getname(node.ret, symbol_table) if node.ret else 'void'

        # Create a 'proc' type and bind it
        proc_binding = ProcBinding(param_names, return_type)
        symbol_table.bind(node.id, proc_binding)

        # Check the procedure block (function body)
        block_result = node.b.accept(self, proc_table)
        print("Now --------------------------------> checking the body of the function")
        if block_result != 'OK':
            return block_result  # Propagate block-level errors

        # Exit back to the original scope
        print("Symbol table in procedure declaration ------------------------> ",symbol_table.bindings)
        symbol_table.exit()

        # Return 'OK' to indicate a valid procedure declaration
        return 'OK'

    def visitFormalParameters(self, node, symbol_table):
        print_function_name()
        # Initialize lists to collect parameter names and types
        param_names = [param for param in node.params]
        param_types = [type for type in node.types]

        print(f"In creating formal parameters ------------------->\nnames: {param_names}\nTypes:{param_types}")
        # Check for reserved parameter names
        for param in param_names:
            if param in ["int", "float", "void", "string", "bool"]:
                raise Exception(f"Cannot use reserved name '{param}' for a parameter.")

        # Bind the parameter names to their corresponding types
        for i in range(len(param_names)):
            param_name = param_names[i]
            param_type = param_types[i]
            if param_type == 'float':
                symbol_table.bind(param_name, FloatBinding(value=0.0))
            elif param_type == 'int':
                symbol_table.bind(param_name, IntBinding(value=0))
            elif param_type == 'string':
                symbol_table.bind(param_name, StringBinding())
            elif param_type == 'bool':
                symbol_table.bind(param_name, BoolBinding())
            else:
                raise Exception(f"Undefined type '{param_type}' for parameter '{param_name}'")

        # Return the list of parameter names
        return param_names

    def visitStatement(self, node, arg=None):
        result = ""
        if node.assign:
            result = node.assign.accept(self, arg)
        if node.call:
            result = node.call.accept(self, arg)
        if node.ret:
            result = node.ret.accept(self, arg)
        if node.ifs:
            result = node.ifs.accept(self, arg)
        if node.whiles:
            result = node.whiles.accept(self, arg)
        return result
    
    def visitAssignmentStatement(self, node, symbol_table):
        print_function_name()
        # Look up the ID in the symbol table
        print("lhs: ", node.id)
        id_type = self.getname(node.id, symbol_table)
        print("lhs type: ", id_type)
        # Check if the ID is declared
        if id_type == 'error':
            return f"Error: '{node.id}' undeclared."

        # Get the type of the expression (right-hand side)
        expr_type = node.e.accept(self, symbol_table)

        # Check if the types match
        if id_type != expr_type:
            return f"Error: '{node.id}' has type '{id_type}' but trying to assign type '{expr_type}'."

        # Return "OK" to indicate a valid assignment
        return "OK"

    def visitReturnStatement(self, node, symbol_table):
        print_function_name()
        # Visit the expression in the return statement
        return_type = node.e.accept(self, symbol_table)

        # Return the type of the expression
        return return_type

    def visitIfStatement(self, node, symbol_table):
        print_function_name()
        # Check the condition
        condition_type = node.c.accept(self, symbol_table)

        # Ensure the condition is of type 'bool'
        if condition_type != 'bool':
            return "Error: Condition in 'if' statement must be of type 'bool'."

        # Check everything in the 'then' branch
        then_result = node.t.accept(self, symbol_table)

        # Check everything in the 'else' branch, if it exists
        if node.f:
            else_result = node.f.accept(self, symbol_table)
            # Return the type of 'Statement2' (the 'else' branch)
            return else_result

        # Return the type of 'Statement1' (the 'then' branch) if there is no 'else' branch
        return then_result

    def visitWhileStatement(self, node, symbol_table):
        print_function_name()
        # Check the condition in the while loop
        condition_type = node.c.accept(self, symbol_table)

        # Ensure the condition is of type 'bool'
        if condition_type != 'bool':
            return "Error: Condition in 'while' loop must be of type 'bool'."

        # Check everything within the 'while' loop
        statement_result = node.s.accept(self, symbol_table)

        # Return the type of 'Statement'
        return statement_result

    def visitCondition(self, node, symbol_table):
        print_function_name()
        # Check both sides of the condition
        type1 = node.lhs.accept(self, symbol_table)
        type2 = node.rhs.accept(self, symbol_table)

        # Ensure both sides are of the same type
        if type1 != type2:
            return "Error: Operands in the condition are not of the same type."

        # Return the type 'bool' if the types match
        return 'bool'

    def visitExpression(self, node, symbol_table):
        print_function_name()
        # Check the left side of the expression
        left_type = node.t.accept(self, symbol_table)

        # Check the right side of the expression (if it exists)
        right_type = None
        if node.e:
            right_type = node.e.accept(self, symbol_table)

            # Ensure the types are compatible
            if node.op in ('+', '-', '*', '/'):
                if left_type not in ('int', 'float') or right_type not in ('int', 'float'):
                    return f"Error: Unsupported operand types for '{node.op}' (left: {left_type}, right: {right_type})."
            elif node.op in ('==', '!=', '<', '<=', '>', '>='):
                if left_type != right_type:
                    return f"Error: Operands in comparison have different types (left: {left_type}, right: {right_type})."
            else:
                return f"Error: Unknown operator '{node.op}'."

        # Determine the resulting type of the expression
        if node.op in ('+', '-', '*', '/'):
            # Arithmetic operations yield either 'int' or 'float'
            return 'int' if left_type == 'int' and right_type == 'int' else 'float'
        elif node.op in ('==', '!=', '<', '<=', '>', '>='):
            # Comparison operations yield 'bool'
            return 'bool'

    def visitTerm(self, node, symbol_table):
        print_function_name()
        # Check the left side of the term
        print("Symbol table binding: ", symbol_table.bindings)
        left_type = node.f.accept(self, symbol_table)
        print("left type: ", str(left_type))
        # Check the right side of the term (if it exists)
        right_type = None
        if node.t:
            right_type = node.t.accept(self, symbol_table)

            # Ensure both sides are of the same type
            if left_type != right_type:
                return "Error: Operands in the term are not of the same type."

        # Ensure the type is either 'int' or 'float'
        if left_type not in ('int', 'float'):
            return f"Error: Unsupported operand type for '{node.op}'."

        # Return the type if the types match and are 'int' or 'float'
        return left_type

    def visitFactor(self, node, symbol_table):
        print_function_name()
        if node.id:
            # Handle a factor with an ID (variable)
            var_type = self.visitID(node.id, symbol_table)
            if var_type == 'error':
                return f"Error: Variable '{node.id}' undeclared."
            return var_type
        elif node.int:
            # Handle a factor with an integer literal
            return 'int'
        elif node.float:
            # Handle a factor with a floating-point literal
            return 'float'
        elif node.str:
            # Handle a factor with a string literal
            return 'string'
        elif node.f:
            # Handle a factor with an expression (parenthesized)
            return node.f.accept(self, symbol_table)
        elif node.call:
            # Handle a factor with a function call
            return node.call.accept(self, symbol_table)
        else:
            return 'error'  # Handle any other factor type

    def visitID(self, node, symbol_table):
        print_function_name()
        # Look up the variable name in the symbol table
        var_type = self.getname(node, symbol_table)
        if var_type == 'error':
            return f"Error: Variable '{node}' undeclared."

        # Return the variable's type
        return var_type

    def visitNUM_INT(self, node, symbol_table):
        print_function_name()
        # Return the type 'int' for integer literals
        return 'int'

    def visitNUM_FLOAT(self, node, symbol_table):
        print_function_name()
        # Return the type 'float' for floating-point literals
        return 'float'

    def visitSTR(self, node, symbol_table):
        print_function_name()
        # Return the type 'string' for string literals
        return 'string'

    def visitParenthesisFactor(self, node, symbol_table):
        print_function_name()
        # Visit the enclosed expression within the parentheses
        enclosed_expression_type = node.e.accept(self, symbol_table)

        # Return the type of the enclosed expression
        return enclosed_expression_type

    def visitCallExpression(self, node, symbol_table):
        print_function_name()
        # Lookup the function or procedure in the symbol table
        print("node.id: ", node.id)
        proc_type = self.getname(node.id, symbol_table)

        # Check if the function or procedure exists
        if proc_type == 'error':
            return f"Error: '{node.id}' is not a procedure."
        print(f" node: {str(node)}")
        print(f" node.params: {str(node.params)}")
        print(f" node.params.params:{str(node.params.params)}") # list of expressions

        # Collect argument types
        for exp in node.params.params:
            print(f"Expression t: {exp.t} ")  # term
            print(f"term.f : {exp.t.f}")
            print(f"factor.id: {exp.t.f.id}")
            print(f"factor.int: {exp.t.f.int}")
            print(f"factor.float: {exp.t.f.float}")
            print(f"term.op : {exp.t.op}")
            print(f"term.t : {exp.t.t}")       
            print(f"Expression op: {exp.op} ")
            print(f"Expression e: {exp.e} ")
        args_types = [get_type_from_expression(exp) for exp in node.params.params]

        # Get the formal return type of the procedure
        print("param types: ", args_types)
        print("Function inside symbol table: ", symbol_table.lookup(node.id)) #procBinding
        formal_return_type = symbol_table.lookup(node.id).return_type
        print(f"types_formal_params ----------------------------> {types_formal_params}")
        # Check if the number of arguments matches the number of parameters
        if len(args_types) != len(formal_return_type.params):
            return f"Procedure '{node.id}' requires {len(formal_return_type.params)} parameters but given {len(args_types)}."

        # Return the formal return type of the procedure
        return formal_return_type.return_type

    def visitActualParameters(self, node, symbol_table):
        print_function_name()
        # Initialize an empty list to store parameter types
        parameter_types = []

        # Iterate through each expression in the list
        for expr in node.params:
            # Check each expression and get its type
            expr_type = expr.accept(self, symbol_table)
            parameter_types.append(expr_type)

        # Return the list/tuple of parameter types
        return parameter_types

