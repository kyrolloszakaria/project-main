from asts import AbstractVisitor
from syms import SymbolTable


class Project3Visitor(AbstractVisitor):
    def getname(self, name):
        pass

    def visitProgram(self, node, arg: SymbolTable):
        pass
