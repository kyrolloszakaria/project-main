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
                return 'error'  # Handle undeclared or unknown types
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
            return f"{node.id} already exists"
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
        print("before symbol_table.bind()")
        symbol_table.bind(node.id, FloatBinding(value=0.0) if expr_type == 'float' else IntBinding(value=0))
        # Return the type of the variable
        return "OK"

    def visitProcedureDeclaration(self, node, symbol_table):
        print_function_name()
        # Enter a new scope
        proc_table = symbol_table.enter()

        # Ensure the name ID1 is not a type name
        if self.getname(node.id, symbol_table) != 'error':
            return f"Error: Cannot use reserved name '{node.id}' for a procedure."

        # Get the type of the parameters
        param_types = []
        if node.params:
            param_types = [param.accept(self, proc_table) for param in node.params]

        # Get the return type from ID2 or use 'void' if none is given
        return_type = self.getname(node.type, symbol_table) if node.type else 'void'

        # Create a 'proc' type and bind it
        proc_binding = ProcBinding(param_types, return_type)
        symbol_table.bind(node.id, proc_binding)

        # Check the block
        block_result = node.b.accept(self, proc_table)
        if block_result != 'OK':
            return block_result  # Propagate block-level errors

        # Exit back to the original scope
        symbol_table.exit()

        # Return the function's type ('proc')
        return 'proc'

    def visitFormalParameters(self, node, symbol_table):
        print_function_name()
        # Initialize a list to collect parameter types
        param_types = []

        for param in node.params:
            # Ensure none of the names `ID1` are type names
            if self.getname(param.id, symbol_table) != 'error':
                return f"Error: Cannot use reserved name '{param.id}' for a parameter."

            # Collect the parameter's type
            param_type = self.getname(param.type, symbol_table)
            param_types.append(param_type)

        # Return the list or tuple of parameter types
        return tuple(param_types)  # You can use list() if you prefer a list

    def visitAssignmentStatement(self, node, symbol_table):
        print_function_name()
        # Look up the ID in the symbol table
        id_type = self.getname(node.id, symbol_table)
        if id_type == 'error':
            return f"Error: Variable '{node.id}' undeclared."

        # Get the type of the expression
        expr_type = node.e.accept(self, symbol_table)

        # Check if the types match
        if id_type != expr_type:
            return f"Error: Variable '{node.id}' has type '{id_type}' but trying to assign type '{expr_type}'."

        # Return the type
        return id_type

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

        # Check everything in the 'else' branch
        else_result = node.f.accept(self, symbol_table)

        # Return the type of 'Statement2' (the 'else' branch)
        return else_result

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

            # Ensure both sides are of the same type
            if left_type != right_type:
                return f"Error: Operands in the expression are not of the same type: {left_type} and {right_type}."

            # Check the operator's compatibility with the operand types
            if node.op in ('+', '-', '*', '/'):
                if left_type not in ('int', 'float'):
                    return f"Error: Unsupported operand type for '{node.op}'."
            else:
                return f"Error: Unknown operator '{node.op}'."

        # Return the resulting type of the expression
        return left_type


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
            var_type = self.getname(node.id, symbol_table)
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
    # Visit method for ID
    def visitID(self, node, symbol_table):
        print_function_name()
        # Look up the variable name in the symbol table
        var_type = self.getname(node.id, symbol_table)
        if var_type == 'error':
            return f"Error: Variable '{node.id}' undeclared."
        
        # Return the variable's type
        return var_type

    # Visit method for NUM_INT
    def visitNUM_INT(self, node, symbol_table):
        print_function_name()
        # Return the type 'int' for integer literals
        return 'int'

    # Visit method for NUM_FLOAT
    def visitNUM_FLOAT(self, node, symbol_table):
        print_function_name()
        # Return the type 'float' for floating-point literals
        return 'float'

    # Visit method for STR
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
        proc_type = self.getname(node.id, symbol_table)

        # Check if the function or procedure exists
        if proc_type == 'error':
            return f"Error: '{node.id}' is not a procedure."

        # Get the list of parameters and their types
        params = proc_type.params
        param_types = proc_type.types

        # Check if the number of arguments matches the number of parameters
        if len(node.params.params) != len(params):
            return f"Error: Procedure '{node.id}' requires {len(params)} parameters but given {len(node.params.params)}."

        # Check each argument type against its corresponding parameter type
        for arg, param_type in zip(node.params.params, param_types):
            arg_type = arg.accept(self, symbol_table)
            if arg_type != param_type:
                return f"Error: Argument type does not match for procedure '{node.id}'."

        # Return the return type of the procedure
        return proc_type.ret

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
