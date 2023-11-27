from asts import AbstractVisitor


def getBuiltinProcedures():
    return """.method public static _out : (Ljava/lang/String;)V
.code stack 2 locals 1
   getstatic Field java/lang/System out Ljava/io/PrintStream;
   aload_0
   invokevirtual Method java/io/PrintStream println (Ljava/lang/String;)V
   return
.end code
.end method

.method public static _int : (F)I
.code stack 2 locals 1
   fload_0
   f2i
   ireturn
.end code
.end method

.method public static _float : (I)F
.code stack 2 locals 1
   iload_0
   i2f
   freturn
.end code
.end method

.method public static _string : (F)Ljava/lang/String;
.code stack 2 locals 1
   fload_0
   invokestatic Method java/lang/Float toString (F)Ljava/lang/String;
   areturn
.end code
.end method

"""


class Project4Visitor(AbstractVisitor):
    def visitProgram(self, node, *args):
        pass
