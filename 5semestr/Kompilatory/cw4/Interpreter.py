import AST
import SymbolTable
from Memory import *
from Exceptions import *
from visit import *
import operator


class Interpreter(object):
    def __init__(self):
        self.memoryStack = MemoryStack()

    @on('node')
    def visit(self, node):
        pass

    @when(AST.BinExpr)
    def visit(self, node):

        ops = {'+': operator.add,
               '-': operator.sub,
               '*': operator.mul,
               '/': operator.div,
               '%': operator.mod,
               '^': operator.xor,
               '|': operator.or_,
               '&': operator.and_,
               '<': operator.lt,
               '>': operator.gt,
               '==': operator.eq,
               '!=': operator.ne,
               '<=': operator.le,
               '>=': operator.ge,
               '>>': operator.rshift,
               '<<': operator.lshift,
               '&&': operator.and_,
               '||': operator.or_}
        # print "BinExpr"
        r1 = node.left.accept(self)
        r2 = node.right.accept(self)
        return ops[node.op](r1,r2)

    @when(AST.Main)
    def visit(self, node):
        # print "Main"
        node.declarations.accept(self)
        node.fundefs.accept(self)
        node.instructions.accept(self)

    @when(AST.DeclarationsMany)
    def visit(self, node):
        # print "DeclarationsMany"
        node.declarations.accept(self)
        node.declaration.accept(self)

    @when(AST.DeclarationsNone)
    def visit(self, node):
        # print "DeclarationsNone"
        pass

    @when(AST.DeclarationMany)
    def visit(self, node):
        # print "DeclarationMany"
        node.inits.accept(self)

    @when(AST.DeclarationSingle)
    def visit(self, node):
        # print "DeclarationSingle"
        pass

    @when(AST.InitsMany)
    def visit(self, node):
        # print "InitsMany"
        node.inits.accept(self)
        node.init.accept(self)

    @when(AST.InitsSingle)
    def visit(self, node):
        # print "InitsSingle"
        node.init.accept(self)

    @when(AST.Init)
    def visit(self, node):
        # print "Init"
        expression_accept = node.expression.accept(self)
        self.memoryStack.peek().put(node.id, expression_accept)
        return expression_accept

    @when(AST.InstructionsMany)
    def visit(self, node):
        # print "InstructionsMany"
        node.instructions.accept(self)
        node.instruction.accept(self)

    @when(AST.InstructionsSingle)
    def visit(self, node):
        # print "InstructionsSingle"
        node.instruction.accept(self)

    @when(AST.Instruction)
    def visit(self, node):
        # print "Instruction"
        node.instruction.accept(self)

    @when(AST.Print_instr)
    def visit(self, node):
        # print "Print_instr"
        print node.expression.accept(self)

    @when(AST.Labeled_instr)
    def visit(self, node):
        # print "Labeled_instr"
        pass

    @when(AST.Assignment)
    def visit(self, node):
        # print "Assignment"
        expression_accept = node.expression.accept(self)
        self.memoryStack.set(node.id, expression_accept)
        return expression_accept

    @when(AST.Choice_instr)
    def visit(self, node):
        # print "Choice_instr"
        if node.condition.accept(self):
            return node.instruction.accept(self)
        else:
            pass

    @when(AST.Choice_instr_with_else)
    def visit(self, node):
        # print "Choice_instr_with_else"
        if node.condition.accept(self):
            return node.instruction.accept(self)
        else:
            return node.elseinstruction.accept(self)

    @when(AST.While_instr)
    def visit(self, node):
        # print "While_instr"
        while node.condition.accept(self):
            try:
                node.instruction.accept(self)
            except BreakException:
                break
            except ContinueException:
                pass

    @when(AST.Repeat_instr)
    def visit(self, node):
        # print "Repeat_instr"
        while True:
            try:
                node.instructions.accept(self)
                if node.condition.accept(self):
                    break
            except BreakException:
                break
            except ContinueException:
                if node.condition.accept(self):
                    break
                pass

    @when(AST.Return_instr)
    def visit(self, node):
        # print "Return_instr"
        value = node.expression.accept(self)
        raise ReturnValueException(value)

    @when(AST.Continue_instr)
    def visit(self, node):
        # print "Continue_instr"
        raise ContinueException()

    @when(AST.Break_instr)
    def visit(self, node):
        # print "Break_instr"
        raise BreakException()

    @when(AST.Compound_instr)
    def visit(self, node):
        # print "Compound_instr"
        node.declarations.accept(self)
        node.instructions.accept(self)

    @when(AST.Integer)
    def visit(self, node):
        # print "Integer"
        return int(node.const_value[0]);

    @when(AST.Float)
    def visit(self, node):
        # print "Float"
        return float(node.const_value[0])

    @when(AST.String)
    def visit(self, node):
        # print "String"
        return str(node.const_value[0][1:-1])

    @when(AST.ExpressionSimple)
    def visit(self, node):
        # print "ExpressionSimple"
        if isinstance(node.id, str):  # ID
            return self.memoryStack.get(node.id)
        else:  # Const
            return self.id.accept(self)

    @when(AST.ExprInBrackets)
    def visit(self, node):
        # print "ExprInBrackets"
        return node.expression.accept(self)

    @when(AST.Funcalls)
    def visit(self, node):
        # print "Funcalls"
        fun = self.memoryStack.get(node.id)
        funMemory = Memory(node.id)
        if node.expr_list_or_empty is not None:
            for argExpr, actualArg in zip(node.expr_list_or_empty.children, fun.arg_list.children):
                funMemory.put(actualArg.accept(self), argExpr.accept(self))
        self.memoryStack.push(funMemory)
        try:
            fun.compound_instr.accept(self)
        except ReturnValueException as e:
            return e.value
        finally:
            self.memoryStack.pop()

    @when(AST.ExpressionList)
    def visit(self, node):
        # print "ExpressionList"
        for child in node.children:
            child.accept(self)

    @when(AST.Fundefs_many)
    def visit(self, node):
        # print "Fundefs_many"
        node.fundef.accept(self)
        node.fundefs.accept(self)

    @when(AST.Fundef)
    def visit(self, node):
        # print "Fundef"
        self.memoryStack.peek().put(node.id, node)

    @when(AST.ArgumentList)
    def visit(self, node):
        # print "ArgumentList"
        for child in node.children:
            child.accept(self)

    @when(AST.Arg)
    def visit(self, node):
        # print "Arg"
        return node.id
