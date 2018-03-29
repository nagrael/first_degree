import AST

BREAKS = "| "


def addToClass(cls):
    def decorator(func):
        setattr(cls, func.__name__, func)
        return func
    return decorator


class TreePrinter:

    @addToClass(AST.Node)
    def printTree(self, breaks=0):
        raise Exception("printTree not defined in class " + self.__class__.__name__)

    @addToClass(AST.Const)
    def printTree(self, breaks=0):
        return BREAKS * breaks + str(self.value) + "\n"

    @addToClass(AST.ExpressionList)
    def printTree(self, breaks=0):
        return "".join(map(lambda x: x.printTree(breaks + 1), self.expressionList))

    @addToClass(AST.ArgumentList)
    def printTree(self, breaks=0):
        return "".join(map(lambda x: x.printTree(breaks), self.argList))

    @addToClass(AST.Argument)
    def printTree(self, breaks=0):
        return BREAKS * breaks + "ARG " + self.name + "\n"

    @addToClass(AST.BinExpression)
    def printTree(self, breaks=0):
        return BREAKS * breaks + self.op + "\n" + self.lhs.printTree(breaks + 1) + self.rhs.printTree(breaks + 1)

    @addToClass(AST.GroupedExpression)
    def printTree(self, breaks=0):
        return self.interior.printTree(breaks)

    @addToClass(AST.CompoundInstruction)
    def printTree(self, breaks=0):
        return ("" if self.declarations is None else self.declarations.printTree(breaks + 1)) + \
            self.instructions.printTree(breaks + 1)

    @addToClass(AST.LabeledInstruction)
    def printTree(self, breaks=0):
        return BREAKS * breaks + "LABEL\n" + BREAKS * (breaks + 1) + str(self.id) + "\n" + \
               self.instr.printTree(breaks + 1)

    @addToClass(AST.FunctionCallExpression)
    def printTree(self, breaks=0):
        return BREAKS * breaks + "FUNCALL\n" + BREAKS * (breaks + 1) + str(self.name) + "\n" + \
               self.args.printTree(breaks+1)

    @addToClass(AST.FunctionDefinitionList)
    def printTree(self, breaks=0):
        return "".join(map(lambda x: x.printTree(breaks), self.fundefs))

    @addToClass(AST.FunctionDefinition)
    def printTree(self, breaks=0):
        return BREAKS * breaks + "FUNDEF\n" + BREAKS * (breaks + 1) + str(self.name) + "\n" + \
               BREAKS * (breaks + 1) + "RET " + str(self.retType) + "\n" + self.args.printTree(breaks + 1) + \
               self.body.printTree(breaks)

    @addToClass(AST.DeclarationList)
    def printTree(self, breaks=0):
        return BREAKS * breaks + "DECL\n" + "".join(map(lambda x: x.printTree(breaks + 1), self.declarations))

    @addToClass(AST.Declaration)
    def printTree(self, breaks=0):
        return self.inits.printTree(breaks)

    @addToClass(AST.InitList)
    def printTree(self, breaks=0):
        return "".join(map(lambda x: x.printTree(breaks), self.inits))

    @addToClass(AST.Init)
    def printTree(self, breaks=0):
        return BREAKS * breaks + "=\n" + BREAKS * (breaks + 1) + str(self.name) + "\n" + \
               self.expr.printTree(breaks + 1)

    @addToClass(AST.InstructionList)
    def printTree(self, breaks=0):
        return "".join(map(lambda x: x.printTree(breaks), self.instructions))

    @addToClass(AST.PrintInstruction)
    def printTree(self, breaks=0):
        return BREAKS * breaks + "PRINT\n" + self.expr.printTree(breaks + 1)

    @addToClass(AST.Assignment)
    def printTree(self, breaks=0):
        return BREAKS * breaks + "=\n" + BREAKS * (breaks + 1) + str(self.id) + "\n" + \
               self.expr.printTree(breaks + 1)

    @addToClass(AST.ChoiceInstruction)
    def printTree(self, breaks=0):
        return BREAKS * breaks + "IF\n" + self.condition.printTree(breaks + 1) + self.action.printTree(breaks + 1) + \
               ("" if self.alternateAction is None else BREAKS * breaks + "ELSE\n" +
                                                        self.alternateAction.printTree(breaks + 1))

    @addToClass(AST.WhileInstruction)
    def printTree(self, breaks=0):
        return BREAKS * breaks + "WHILE\n" + self.condition.printTree(breaks + 1) + self.instruction.printTree(breaks)

    @addToClass(AST.RepeatInstruction)
    def printTree(self, breaks=0):
        return BREAKS * breaks + "REPEAT\n" + self.instructions.printTree(breaks + 1) + BREAKS * breaks + \
            "UNTIL\n" + self.condition.printTree(breaks + 1)

    @addToClass(AST.ReturnInstruction)
    def printTree(self, breaks=0):
        return BREAKS * breaks + "RETURN\n" + self.expression.printTree(breaks + 1)

    @addToClass(AST.BreakInstruction)
    def printTree(self, breaks=0):
        return BREAKS * breaks + "BREAK\n"

    @addToClass(AST.ContinueInstruction)
    def printTree(self, breaks=0):
        return BREAKS * breaks + "CONTINUE\n"

    @addToClass(AST.Program)
    def printTree(self, breaks=0):
        return ("" if self.declarations is None else self.declarations.printTree(breaks)) + \
               ("" if self.fundefs_opt is None else self.fundefs_opt.printTree(breaks)) + \
               self.instructions.printTree(breaks)