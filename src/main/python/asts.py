class AbstractNode:
    def accept(self, v, arg=None):
        print("Now we are visiting ", self.__class__.__name__ )
        func = getattr(v, 'visit' + self.__class__.__name__)
        return func(self, arg)


class AbstractVisitor:
    def visitProgram(self, node, arg=None):
        if node.b:
            node.b.accept(self, arg)

    def visitBlock(self, node, arg=None):
        if node.decls:
            for d in node.decls:
                if d:
                    d.accept(self, arg)
        if node.stmts:
            for s in node.stmts:
                if s:
                    s.accept(self, arg)

    def visitVariableDeclaration(self, node, arg=None):
        if node.rhs:
            node.rhs.accept(self, arg)

    def visitProcedureDeclaration(self, node, arg=None):
        if node.params:
            node.params.accept(self, arg)
        if node.b:
            node.b.accept(self, arg)

    def visitFormalParameters(self, node, arg=None):
        pass

    def visitStatement(self, node, arg=None):
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

    def visitAssignmentStatement(self, node, arg=None):
        if node.e:
            node.e.accept(self, arg)

    def visitCallExpression(self, node, arg=None):
        if node.params:
            node.params.accept(self, arg)

    def visitReturnStatement(self, node, arg=None):
        if node.e:
            node.e.accept(self, arg)

    def visitIfStatement(self, node, arg=None):
        if node.c:
            node.c.accept(self, arg)
        if node.t:
            node.t.accept(self, arg)
        if node.f:
            node.f.accept(self, arg)

    def visitWhileStatement(self, node, arg=None):
        if node.c:
            node.c.accept(self, arg)
        if node.s:
            node.s.accept(self, arg)

    def visitActualParameters(self, node, arg=None):
        if node.params:
            for e in node.params:
                if e:
                    e.accept(self, arg)

    def visitCondition(self, node, arg=None):
        if node.lhs:
            node.lhs.accept(self, arg)
        if node.rhs:
            node.rhs.accept(self, arg)

    def visitExpression(self, node, arg=None):
        if node.t:
            node.t.accept(self, arg)
        if node.e:
            node.e.accept(self, arg)

    def visitTerm(self, node, arg=None):
        if node.f:
            node.f.accept(self, arg)
        if node.t:
            node.t.accept(self, arg)

    def visitFactor(self, node, arg=None):
        if node.f:
            node.f.accept(self, arg)
        if node.call:
            node.call.accept(self, arg)

    def visitParenthesisFactor(self, node, arg=None):
        if node.e:
            node.e.accept(self, arg)


class ActualParameters(AbstractNode):
    def __init__(self):
        self.params = []


class AssignmentStatement(AbstractNode):
    def __init__(self):
        self.id = None
        self.e = None


class Block(AbstractNode):
    def __init__(self):
        self.decls = []
        self.stmts = []


class CallExpression(AbstractNode):
    def __init__(self):
        self.id = None
        self.params = []


class Condition(AbstractNode):
    def __init__(self):
        self.lhs = None
        self.op = None
        self.rhs = None


class Expression(AbstractNode):
    def __init__(self):
        self.t = None
        self.op = None
        self.e = None


class Factor(AbstractNode):
    def __init__(self):
        self.id = None
        self.int = None
        self.float = None
        self.str = None
        self.f = None
        self.call = None


class FormalParameters(AbstractNode):
    def __init__(self):
        self.params = []
        self.types = []


class IfStatement(AbstractNode):
    def __init__(self):
        self.c = None
        self.t = None
        self.f = None


class ParenthesisFactor(AbstractNode):
    def __init__(self):
        self.e = None


class ProcedureDeclaration(AbstractNode):
    def __init__(self):
        self.id = None
        self.params = []
        self.ret = None
        self.b = None


class Program(AbstractNode):
    def __init__(self):
        self.b = None


class ReturnStatement(AbstractNode):
    def __init__(self):
        self.e = None


class Statement(AbstractNode):
    def __init__(self):
        self.assign = None
        self.call = None
        self.ret = None
        self.ifs = None
        self.whiles = None


class Term(AbstractNode):
    def __init__(self):
        self.f = None
        self.op = None
        self.t = None


class VariableDeclaration(AbstractNode):
    def __init__(self):
        self.id = None
        self.type = None
        self.rhs = None


class WhileStatement(AbstractNode):
    def __init__(self):
        self.c = None
        self.s = None
