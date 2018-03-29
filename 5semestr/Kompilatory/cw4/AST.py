
class Node:

    def __str__(self):
        return self.printTree(0)

    def accept(self, visitor):
        return visitor.visit(self)

    def accept2(self, visitor):
        className = self.__class__.__name__
        meth = getattr(visitor, 'visit_' + className, None)
        if meth is not None:
            return meth(self)


class Main(Node):
    def __init__(self, lineno, declarations, fundefs, instructions):
        self.lineno = lineno
        self.declarations = declarations
        self.fundefs = fundefs
        self.instructions = instructions


class Declarations(Node):
    pass


class DeclarationsMany(Declarations):
    def __init__(self, lineno,  declarations, declaration):
        self.lineno = lineno
        self.declarations = declarations
        self.declaration = declaration


class DeclarationsNone(Declarations):
    def __init__(self, lineno):
        self.lineno = lineno


class Declaration(Node):
    pass


class DeclarationMany(Declaration):
    def __init__(self, lineno,  type, inits):
        self.lineno = lineno
        self.type = type
        self.inits = inits


class DeclarationSingle(Declaration):
    def __init__(self, lineno,  type):
        self.lineno = lineno
        self.type = type


class Inits(Node):
    pass


class InitsMany(Inits):
    def __init__(self, lineno,  init, inits):
        self.lineno = lineno
        self.init = init
        self.inits = inits


class InitsSingle(Inits):
    def __init__(self, lineno,  init):
        self.lineno = lineno
        self.init = init
        self.inits = None


class Init(Node):
    def __init__(self, lineno, id, expression):
        self.lineno = lineno
        self.id = id
        self.expression = expression


class Instructions(Node):
    pass


class InstructionsMany(Instructions):
    def __init__(self, lineno, instruction, instructions):
        self.lineno = lineno
        self.instructions = instructions
        self.instruction = instruction


class InstructionsSingle(Instructions):
    def __init__(self, lineno, instruction):
        self.lineno = lineno
        self.instruction = instruction


class Instruction(Node):
    def __init__(self, lineno, instruction):
        self.lineno = lineno
        self.instruction = instruction


class Print_instr(Node):
    def __init__(self, lineno, expression):
        self.lineno = lineno
        self.expression = expression


class Labeled_instr(Node):
    def __init__(self, lineno, id, instruction):
        self.lineno = lineno
        self.id = id
        self.instruction = instruction


class Assignment(Node):
    def __init__(self, lineno, id, expression):
        self.lineno = lineno
        self.id = id
        self.expression = expression


class Choice_instr(Node):
    def __init__(self, lineno, condition, instruction):
        self.lineno = lineno
        self.condition = condition
        self.instruction = instruction


class Choice_instr_with_else(Node):
    def __init__(self, lineno, condition, instruction, elseinstruction):
        self.lineno = lineno
        self.condition = condition
        self.instruction = instruction
        self.elseinstruction = elseinstruction


class While_instr(Node):
    def __init__(self, lineno, condition, instruction):
        self.lineno = lineno
        self.condition = condition
        self.instruction = instruction


class Repeat_instr(Node):
    def __init__(self, lineno, instructions, condition):
        self.lineno = lineno
        self.instructions = instructions
        self.condition = condition


class Return_instr(Node):
    def __init__(self, lineno, expression):
        self.lineno = lineno
        self.expression = expression


class Continue_instr(Node):
    pass


class Break_instr(Node):
    pass


class Compound_instr(Node):
    def __init__(self, lineno, declarations, instructions):
        self.lineno = lineno
        self.declarations = declarations
        self.instructions = instructions

class Const(Node):
    pass


class Integer(Const):
    def __init__(self, lineno, const_value):
        self.lineno = lineno
        self.const_value = const_value


class Float(Const):
    def __init__(self, lineno, const_value):
        self.lineno = lineno
        self.const_value = const_value


class String(Const):
    def __init__(self, lineno, const_value):
        self.lineno = lineno
        self.const_value = const_value


class Expression(Node):
    pass


class ExpressionSimple(Expression):
    def __init__(self, lineno, id):
        self.lineno = lineno
        self.id = id


class BinExpr(Expression):
    def __init__(self, lineno, left, op,  right):
        self.lineno = lineno
        self.op = op
        self.left = left
        self.right = right


class Funcalls(Node):
    def __init__(self, lineno, id, expr_list_or_empty):
        self.lineno = lineno
        self.id = id
        self.expr_list_or_empty = expr_list_or_empty


class ExprInBrackets(Node):
    def __init__(self, lineno, expression):
        self.lineno = lineno
        self.expression = expression

class ExpressionList(Node):
    def __init__(self):
        self.children = []

    def addExpression(self, expr):
        self.children.append(expr)

class Fundefs(Node):
    def __init__(self, lineno):
        self.lineno = lineno


class Fundefs_many(Node):
    def __init__(self, lineno, fundef, fundefs):
        self.lineno = lineno
        self.fundef = fundef
        self.fundefs = fundefs


class Fundef(Node):
    def __init__(self, lineno, type, id, args_list_or_empty, compound_instruction):
        self.lineno = lineno
        self.type = type
        self.id = id
        self.arg_list = args_list_or_empty
        self.compound_instr = compound_instruction


class ArgumentList(Node):
    def __init__(self):
        self.children = []

    def addArgument(self, arg):
        self.children.append(arg)


class Arg(Node):
    def __init__(self, lineno, type, id):
        self.lineno = lineno
        self.type = type
        self.id = id

