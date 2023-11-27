class Node:
    def accept(self, v, arg):
        pass

class AbstractVisitor:
    pass


class ProgramNode(Node):
    def __init__(self, block_node):
        self.block_node = block_node

    def accept(self, visitor, arg):
        return visitor.visit_program_node(self, arg)

class BlockNode:
    def __init__(self, nodes):
        self.nodes = nodes
    def accept(self, visitor, arg):
        return visitor.visit_block_node(self, arg)

class VariableDeclarationNode(Node):
    def __init__(self, identifier, expression):
        super().__init__()  # This calls the initializer of the parent (Node) class.
        self.identifier = identifier
        self.expression = expression

    def accept(self, visitor, arg):
        return visitor.visit_variable_declaration_node(self, arg)

    def __str__(self):  # This method is just for debugging, it helps print the node.
        return f"VariableDeclaration({self.identifier} = {self.expression})"

class ProcedureDeclarationNode(Node):
    def __init__(self, identifier, formal_parameters, block):
        self.identifier = identifier
        self.formal_parameters = formal_parameters  # This can be None or an instance of FormalParametersNode (or its equivalent).
        self.block = block  # This should be an instance of BlockNode

    def accept(self, visitor, arg):
        return visitor.visit_procedure_declaration_node(self, arg)
    
class FormalParametersNode(Node):
    def __init__(self, parameters):
        """
        Initializes the FormalParametersNode.

        :param parameters: A list of tuples where each tuple represents (identifier, type).
        """
        self.parameters = parameters

    def accept(self, visitor, arg):
        return visitor.visit_formal_parameters_node(self, arg)

class AssignmentStatementNode(Node):
    def __init__(self, identifier, expression):
        """
        Initializes the AssignmentStatementNode.

        :param identifier: The name of the variable being assigned to.
        :param expression: The value being assigned.
        """
        self.identifier = identifier
        self.expression = expression

    def accept(self, visitor, arg):
        return visitor.visit_assignment_statement_node(self, arg)

class ReturnStatementNode(Node):
    def __init__(self, expression):
        """
        Initializes the ReturnStatementNode.

        :param expression: The value or expression being returned.
        """
        self.expression = expression

    def accept(self, visitor, arg):
        return visitor.visit_return_statement_node(self, arg)

class IfStatementNode(Node):
    def __init__(self, condition, then_statement, else_statement):
        """
        Initializes the IfStatementNode.

        :param condition: The condition for the if statement.
        :param then_statement: The statement to execute if the condition is True.
        :param else_statement: The statement to execute if the condition is False.
        """
        self.condition = condition
        self.then_statement = then_statement
        self.else_statement = else_statement

    def accept(self, visitor, arg):
        return visitor.visit_if_statement_node(self, arg)

class WhileStatementNode(Node):
    def __init__(self, condition, loop_statement):
        """
        Initializes the WhileStatementNode.

        :param condition: The condition for the while loop.
        :param loop_statement: The statement to execute while the condition is True.
        """
        self.condition = condition
        self.loop_statement = loop_statement

    def accept(self, visitor, arg):
        return visitor.visit_while_statement_node(self, arg)

class ConditionNode(Node):
    def __init__(self, left_expression, op, right_expression):
        """
        Initializes the ConditionNode.

        :param left_expression: The left-hand side expression.
        :param op: The relational operator.
        :param right_expression: The right-hand side expression.
        """
        self.left_expression = left_expression
        self.op = op
        self.right_expression = right_expression

    def accept(self, visitor, arg):
        return visitor.visit_condition_node(self, arg)
    
class ExpressionNode(Node):
    def __init__(self, left_term, op, right_term):
        """
        Initializes the ExpressionNode.

        :param left_term: The left-hand side term.
        :param op: The arithmetic operator.
        :param right_term: The right-hand side term.
        """
        self.left_term = left_term
        self.op = op
        self.right_term = right_term

    def accept(self, visitor, arg):
        return visitor.visit_expression_node(self, arg)

class TermNode(Node):
    def __init__(self, left_factor, op, right_factor):
        self.left_factor = left_factor
        self.op = op
        self.right_factor = right_factor

    def accept(self, visitor, arg):
        return visitor.visit_term_node(self, arg)
    
class FactorNode(Node):
    def __init__(self, value, factor_type):
        """
        Initializes the FactorNode.

        :param value: The value of the factor (could be ID, int, or float).
        :param factor_type: The type of the factor ("ID", "INT", or "FLOAT").
        """
        self.value = value
        self.factor_type = factor_type

    def accept(self, visitor, arg):
        return visitor.visit_factor_node(self, arg)

class ParenthesisFactorNode(Node):
    def __init__(self, expression):
        self.expression = expression

    def accept(self, visitor, arg):
        return visitor.visit_parenthesis_factor_node(self, arg)

class CallExpressionNode:
    def __init__(self, identifier, actual_parameters):
        self.identifier = identifier
        self.actual_parameters = actual_parameters

    def accept(self, visitor, arg):
        return visitor.visit_call_expression_node(self, arg)


class ActualParametersNode:
    def __init__(self, parameters):
        self.parameters = parameters

    def accept(self, visitor, arg):
        return visitor.visit_actual_parameters_node(self, arg)
