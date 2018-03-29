class Node(object):
    def __str__(self):
        return self.printTree()


class Const(Node):
    def __init__(self, value):
        self.value = value


class Integer(Const):
    pass


class Float(Const):
    pass


class String(Const):
    pass


class Variable(Node):
    pass


class Program(Node):
    def __init__(self, declarations, fundefs_opt, instructions):
        self.declarations = declarations
        self.fundefs_opt = fundefs_opt
        self.instructions = instructions


class Declaration(Node):
    def __init__(self, type, inits):
        self.type = type
        self.inits = inits


class DeclarationList(Node):
    def __init__(self):
        self.declarations = []

    def addDeclaration(self, declaration):
        self.declarations.append(declaration)


class FunctionDefinition(Node):
    def __init__(self, retType, name, args, body):
        self.retType = retType
        self.name = name
        self.args = args
        self.body = body


class FunctionDefinitionList(Node):
    def __init__(self):
        self.fundefs = []

    def addFunction(self, fundef):
        self.fundefs.append(fundef)


class ExpressionList(Node):
    def __init__(self):
        self.expressionList = []

    def addExpression(self, expr):
        self.expressionList.append(expr)


class Argument(Node):
    def __init__(self, type, name):
        self.type = type
        self.name = name


class ArgumentList(Node):
    def __init__(self):
        self.argList = []

    def addArgument(self, arg):
        self.argList.append(arg)


class BinExpression(Node):
    def __init__(self, lhs, op, rhs):
        self.lhs = lhs
        self.op = op
        self.rhs = rhs


class GroupedExpression(Node):
    def __init__(self, interior):
        self.interior = interior


class FunctionCallExpression(Node):
    def __init__(self, name, args):
        self.name = name
        self.args = args


class InitList(Node):
    def __init__(self):
        self.inits = []

    def addInit(self, init):
        self.inits.append(init)


class Init(Node):
    def __init__(self, name, expr):
        self.name = name
        self.expr = expr


class InstructionList(Node):
    def __init__(self):
        self.instructions = []

    def addInstruction(self, instr):
        self.instructions.append(instr)


class PrintInstruction(Node):
    def __init__(self, expr):
        self.expr = expr


class LabeledInstruction(Node):
    def __init__(self, id, instr):
        self.id = id
        self.instr = instr


class Assignment(Node):
    def __init__(self, id, expr):
        self.id = id
        self.expr = expr


class CompoundInstruction(Node):
    def __init__(self, declarations, instructions):
        self.declarations = declarations
        self.instructions = instructions


class ChoiceInstruction(Node):
    def __init__(self, condition, action, alternateAction=None):
        self.condition = condition
        self.action = action
        self.alternateAction = alternateAction


class WhileInstruction(Node):
    def __init__(self, condition, instruction):
        self.condition = condition
        self.instruction = instruction


class RepeatInstruction(Node):
    def __init__(self, instructions, condition):
        self.instructions = instructions
        self.condition = condition


class ReturnInstruction(Node):
    def __init__(self, expression):
        self.expression = expression


class BreakInstruction(Node):
    pass


class ContinueInstruction(Node):
    pass
