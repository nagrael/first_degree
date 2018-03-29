
import AST

def addToClass(cls):

    def decorator(func):
        setattr(cls, func.__name__, func)
        return func
    return decorator

def addIndent(indent):
    return "| " * indent

class TreePrinter:

    @addToClass(AST.Node)
    def printTree(self):
        raise Exception("printTree not defined in class " + self.__class__.__name__)

    @addToClass(AST.Main)
    def printTree(self, indent):
        result = ""
        if self.declarations is not None:
            result += "DECL\n"
            result += addIndent(indent)
            result += self.declarations.printTree(indent)
        result += addIndent(indent)
        result += self.fundefs.printTree(indent)
        result += addIndent(indent)
        result += self.instructions.printTree(indent)
        return result

    @addToClass(AST.DeclarationsMany)
    def printTree(self, indent):
        result = ""
        result += self.declarations.printTree(indent)
        result += self.declaration.printTree(indent)
        return result

    @addToClass(AST.DeclarationsNone)
    def printTree(self, indent):
        result = ""
        return result

    @addToClass(AST.DeclarationMany)
    def printTree(self, indent):
        result = ""
        result += self.inits.printTree(indent)
        return result

    @addToClass(AST.DeclarationSingle)
    def printTree(self, indent):
        result = ""
        result += self.type
        result += self.inits.printTree(indent)
        return result

    @addToClass(AST.InitsSingle)
    def printTree(self, indent):
        result = ""
        result += self.init.printTree(indent+1)
        return result

    @addToClass(AST.InitsMany)
    def printTree(self, indent):
        result = ""
        if self.inits is not None:
            result += self.inits.printTree(indent)
        result += self.init.printTree(indent+1)
        return result

    @addToClass(AST.Init)
    def printTree(self, indent):
        result = addIndent(indent) + "=\n"
        result += addIndent(indent+1)
        result += self.id
        result += "\n"
        result += self.expression.printTree(indent+1)
        return result

    @addToClass(AST.InstructionsSingle)
    def printTree(self, indent):
        result = ""
        result += self.instruction.printTree(indent)
        return result

    @addToClass(AST.InstructionsMany)
    def printTree(self, indent):
        result = ""
        if self.instructions is not None:
            result += self.instructions.printTree(indent)
        result += self.instruction.printTree(indent)
        return result

    @addToClass(AST.Instruction)
    def printTree(self, indent):
        result = ""
        result += self.instruction.printTree(indent)
        return result

    @addToClass(AST.Print_instr)
    def printTree(self, indent):
        result = ""
        result += addIndent(indent)
        result += "PRINT\n" + self.expression.printTree(indent+1)
        return result

    @addToClass(AST.Labeled_instr)
    def printTree(self, indent):
        result = ""
        return result

    @addToClass(AST.Assignment)
    def printTree(self, indent):
        result = addIndent(indent)
        result += "=\n"
        result += addIndent(indent+1)
        result += self.id + "\n"
        result += self.expression.printTree(indent+1)
        return result

    @addToClass(AST.Choice_instr)
    def printTree(self, indent):
        result = addIndent(indent) + "IF\n"
        result += self.condition.printTree(indent+1)
        result += self.instruction.printTree(indent+1)
        return result

    @addToClass(AST.Choice_instr_with_else)
    def printTree(self, indent):
        result = addIndent(indent) + "IF\n"
        result += self.condition.printTree(indent+1)
        result += self.instruction.printTree(indent+1)
        result += addIndent(indent) + "ELSE\n"
        result += self.elseinstruction.printTree(indent+1)
        return result

    @addToClass(AST.While_instr)
    def printTree(self, indent):
        result = addIndent(indent) + "WHILE\n"
        result += self.condition.printTree(indent+1)
        result += self.instruction.printTree(indent+1)
        return result

    @addToClass(AST.Repeat_instr)
    def printTree(self, indent):
        result = addIndent(indent) + "REPEAT\n"
        result += self.instructions.printTree(indent+1)
        result += addIndent(indent)
        result += "UNTIL\n"
        result += self.condition.printTree(indent+1)
        return result

    @addToClass(AST.Return_instr)
    def printTree(self, indent):
        result = addIndent(indent) + "RETURN\n" + self.expression.printTree(indent+1)
        return result

    @addToClass(AST.Continue_instr)
    def printTree(self, indent):
        result = addIndent(indent) + "CONTINUE\n"
        return result

    @addToClass(AST.Break_instr)
    def printTree(self, indent):
        result = addIndent(indent) + "BREAK\n"
        return result

    @addToClass(AST.Compound_instr)
    def printTree(self, indent):
        result = ""
        if self.declarations is not None:
            if self.declarations.printTree(indent) != "":
                result += addIndent(indent) + "DECL\n"
                result += self.declarations.printTree(indent)
        result += self.instructions.printTree(indent)
        return result

    @addToClass(AST.Integer)
    def printTree(self, indent):
        result = addIndent(indent)
        result += self.const_value[0] + "\n"
        return result

    @addToClass(AST.Float)
    def printTree(self, indent):
        result = addIndent(indent)
        result += self.const_value[0] + "\n"
        return result

    @addToClass(AST.String)
    def printTree(self, indent):
        result = addIndent(indent)
        result += self.const_value[0] + "\n"
        return result

    @addToClass(AST.ExpressionSimple)
    def printTree(self, indent):
        result = ""
        if isinstance(self.id,str):
            result +=addIndent(indent) + self.id+"\n"
        else:
            result += self.id.printTree(indent)
        return result

    @addToClass(AST.BinExpr)
    def printTree(self, indent):
        result = addIndent(indent)
        result += self.op + "\n"
        result += self.left.printTree(indent+1)
        result += self.right.printTree(indent+1)
        return result

    @addToClass(AST.Funcalls)
    def printTree(self, indent):
        result = addIndent(indent) + "FUNCALL\n"
        result += addIndent(indent+1) + self.id +"\n"
        if self.expr_list_or_empty is not None:
            result += self.expr_list_or_empty.printTree(indent+2)
        return result

    @addToClass(AST.ExprInBrackets)
    def printTree(self, indent):
        result = self.expression.printTree(indent)
        return result

    @addToClass(AST.ExpressionList)
    def printTree(self, indent):
        return "".join(map(lambda x: x.printTree(indent), self.children))

    @addToClass(AST.Fundefs)
    def printTree(self, indent):
        result = ""
        return result

    @addToClass(AST.Fundefs_many)
    def printTree(self, indent):
        result = ""
        result += self.fundef.printTree(indent)
        result += self.fundefs.printTree(indent)
        return result

    @addToClass(AST.Fundef)
    def printTree(self, indent):
        result = "FUNDEF\n"
        result += addIndent(indent+1)
        result += self.id + "\n"
        result += addIndent(indent+1)
        result += "RET " + self.type + "\n"
        if self.arg_list is not None:
            result += self.arg_list.printTree(indent+1)
        result += self.compound_instr.printTree(indent+1)
        return result

    @addToClass(AST.ArgumentList)
    def printTree(self, indent):
        return "".join(map(lambda x: x.printTree(indent), self.children))

    @addToClass(AST.Arg)
    def printTree(self, indent):
        result = addIndent(indent) + "ARG " + self.id + "\n"
        return result