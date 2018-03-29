

from SymbolTable import FunctionsTable
from SymbolTable import SymbolTable


class TypeChecker(object):
    errors = []

    def __init__(self):
        self.isValid = True

        self.ttype = {'!=': {'string': {'string': 'string'}, 'int': {'float': 'int', 'int': 'int'},
                             'float': {'int': 'int', 'float': 'int'}},
                      '<': {'string': {'string': 'string'}, 'int': {'float': 'int', 'int': 'int'},
                            'float': {'int': 'int', 'float': 'int'}},
                      '<=': {'string': {'string': 'string'}, 'int': {'float': 'int', 'int': 'int'},
                             'float': {'int': 'int', 'float': 'int'}},
                      '>': {'string': {'string': 'string'}, 'int': {'float': 'int', 'int': 'int'},
                            'float': {'int': 'int', 'float': 'int'}},
                      '>=': {'string': {'string': 'string'}, 'int': {'float': 'int', 'int': 'int'},
                             'float': {'int': 'int', 'float': 'int'}},
                      '==': {'string': {'string': 'string'}, 'int': {'float': 'int', 'int': 'int'},
                             'float': {'int': 'int', 'float': 'int'}},
                      '+': {'string': {'string': 'string'}, 'int': {'float': 'float', 'int': 'int'},
                            'float': {'int': 'float', 'float': 'float'}},
                      '-': {'int': {'int': 'int', 'float': 'float'}, 'float': {'int': 'float', 'float': 'float'}},
                      '*': {'string': {'int': 'string'}, 'int': {'int': 'int', 'float': 'float', 'string': 'string'},
                            'float': {'int:': 'float', 'float': 'float'}},
                      '/': {'int': {'int': 'float', 'float': 'float'}, 'float': {'float': 'float'}},
                      '%': {'int': {'int': 'int'}},
                      '^': {'int': {'int': 'int', 'float': 'float'}, 'float': {'int': 'float', 'float': 'float'}},
                      '&': {'int': {'int': 'int'}},
                      'AND': {'int': {'int': 'int'}},
                      'OR': {'int': {'int': 'int'}},
                      'SHL': {'int': {'int': 'int'}},
                      'SHR': {'int': {'int': 'int'}},
                      'EQ': {'int': {'int': 'int'}},
                      'NEQ': {'int': {'int': 'int'}},
                      'LE': {'int': {'int': 'int'}},
                      'GE': {'int': {'int': 'int'}},
                      }

    def visit_Main(self, node):
        node.Functions = FunctionsTable(None, "Functions")
        node.Variables = SymbolTable(None, "Variables")
        node.declarations.Functions = node.Functions
        node.declarations.Variables = node.Variables
        node.fundefs.Functions = node.Functions
        node.fundefs.Variables = node.Variables
        node.instructions.Functions = node.Functions
        node.instructions.Variables = node.Variables
        node.declarations.accept2(self)
        node.fundefs.accept2(self)
        node.instructions.accept2(self)
        return self.errors

    def visit_DeclarationsMany(self, node):
        node.declarations.Functions = node.Functions
        node.declarations.Variables = node.Variables
        node.declarations.accept2(self)
        node.declaration.Functions = node.Functions
        node.declaration.Variables = node.Variables
        node.declaration.accept2(self)

    def visit_DeclarationsNone(self, node):
        pass

    def visit_DeclarationMany(self, node):
        node.inits.Functions = node.Functions
        node.inits.Variables = node.Variables
        self.visit_InitsMany(node.inits, node.type)

    def visit_DeclarationSingle(self, node):
        pass

    def visit_InitsMany(self, node, type):
        node.init.Functions = node.Functions
        node.init.Variables = node.Variables
        self.visit_Init(node.init, type)
        if node.inits is not None:
            node.inits.Functions = node.Functions
            node.inits.Variables = node.Variables
            self.visit_InitsMany(node.inits, type)

    def visit_InitsSingle(self, node, type):
        node.init.Functions = node.Functions
        node.init.Variables = node.Variables
        self.visit_Init(node.init, type)

    def visit_Init(self, node, type):
        if node.Variables.put(node.id, type) == -1:
            self.errors.append("ERROR In line " + str(node.lineno) + ": Variable " + node.id + " has already been initialized.")

    def visit_InstructionsMany(self, node):
        node.instructions.Functions = node.Functions
        node.instructions.Variables = node.Variables
        node.instructions.accept2(self)
        node.instruction.Functions = node.Functions
        node.instruction.Variables = node.Variables
        node.instruction.accept2(self)

    def visit_InstructionsSingle(self, node):
        node.instruction.Functions = node.Functions
        node.instruction.Variables = node.Variables
        node.instruction.accept2(self)

    def visit_Instruction(self, node):
        node.instruction.Functions = node.Functions
        node.instruction.Variables = node.Variables
        node.instruction.accept2(self)

    def visit_Print_instr(self, node):
        node.expression.Functions = node.Functions
        node.expression.Variables = node.Variables
        node.expression.accept2(self)

    def visit_Labeled_instr(self, node):
        node.instruction.Functions = node.Functions
        node.instruction.Variables = node.Variables
        node.instruction.accept2(self)

    def visit_Assignment(self, node):
        node.expression.Functions = node.Functions
        node.expression.Variables = node.Variables
        type2 = node.expression.accept2(self)
        type1 = node.Variables.get(node.id)
        if type1 == -1:
            self.errors.append("ERROR in line " + str(node.lineno) + ": Variable " + node.id + " was not declared.")
        elif type2 == -1:
            self.errors.append("ERROR in line " + str(node.lineno) + ": Incorrect expression.")
        elif type1 != type2:
            self.errors.append("ERROR In line " + str(node.lineno) + ": Invalid assignment " + str(type2) + " to "+str(type1) + ".")

    def visit_Choice_instr(self, node):
        node.condition.Functions = node.Functions
        node.condition.Variables = node.Variables
        node.condition.accept2(self)
        node.instruction.Functions = FunctionsTable(node.Functions, "Functions")
        node.instruction.Variables = SymbolTable(node.Variables, "Variables")
        node.instruction.accept2(self)

    def visit_Choice_instr_with_else(self, node):
        node.condition.Functions = node.Functions
        node.condition.Variables = node.Variables
        node.condition.accept2(self)
        node.instruction.Functions = FunctionsTable(node.Functions, "Functions")
        node.instruction.Variables = SymbolTable(node.Variables, "Variables")
        node.instruction.accept2(self)
        node.elseinstruction.Functions = FunctionsTable(node.Functions, "Functions")
        node.elseinstruction.Variables = SymbolTable(node.Variables, "Variables")
        node.elseinstruction.accept2(self)

    def visit_While_instr(self, node):
        node.condition.Functions = node.Functions
        node.condition.Variables = node.Variables
        node.condition.accept2(self)
        node.instruction.Functions = FunctionsTable(node.Functions, "Functions")
        node.instruction.Variables = SymbolTable(node.Variables, "Variables")
        node.instruction.accept2(self)

    def visit_Repeat_instr(self, node):
        Functions = FunctionsTable(node.Functions, "Functions")
        Variables = SymbolTable(node.Variables, "Variables")
        node.instructions.Functions = Functions
        node.instructions.Variables = Variables
        node.instructions.accept2(self)
        node.condition.Functions = Functions
        node.condition.Variables = Variables
        node.condition.accept2(self)

    def visit_Return_instr(self, node):
        node.expression.Functions = node.Functions
        node.expression.Variables = node.Variables
        node.expression.accept2(self)

    def visit_Compound_instr(self, node):
        Functions = FunctionsTable(node.Functions, "Functions")
        Variables = SymbolTable(node.Variables, "Variables")
        node.declarations.Functions = Functions
        node.declarations.Variables = Variables
        node.declarations.accept2(self)
        node.instructions.Functions = Functions
        node.instructions.Variables = Variables
        node.instructions.accept2(self)

    def visit_Integer(self, node):
        return node.const_value[1]

    def visit_Float(self, node):
        return node.const_value[1]

    def visit_String(self, node):
        return node.const_value[1]

    def visit_ExpressionSimple(self, node):
        if node.id is not None:
            if node.id.__class__.__name__ in ["Integer", "Float", "String"]:
                node.id.Functions = node.Functions
                node.id.Variables = node.Variables
                return node.id.accept2(self)
            if node.Variables.get(node.id) == -1:
                self.errors.append("ERROR in line " + str(node.lineno) + ": Variable " + node.id
                                   + " was not found in the current scope.")
                return 'int'
            return node.Variables.get(node.id)

    def visit_BinExpr(self, node):
        node.left.Functions = node.Functions
        node.left.Variables = node.Variables
        type1 = node.left.accept2(self)
        node.right.Functions = node.Functions
        node.right.Variables = node.Variables
        type2 = node.right.accept2(self)
        if node.op in self.ttype.keys() and type1 in self.ttype[node.op].keys() \
                and type2 in self.ttype[node.op][type1].keys():
            return self.ttype[node.op][type1][type2]
        else:
            self.errors.append("ERROR in line " + str(node.lineno) + ": Invalid expression: "+str(type1) + node.op + str(type2))
            return 'int'

    def visit_ExprInBrackets(self, node):
        node.expression.Functions = node.Functions
        node.expression.Variables = node.Variables
        return node.expression.accept2(self)

    def visit_Funcalls(self, node):
        type1 = node.Functions.get(node.id)
        if(type1 == -1):
            self.isValid = False
            self.errors.append("ERROR in line " + str(node.lineno) + ": Function not found.")
            return type1
        if node.expr_list_or_empty is not None: #if function was invoked with at least one argument
            node.expr_list_or_empty.Functions = node.Functions
            node.expr_list_or_empty.Variables = node.Variables
            types = []
            type2 = node.expr_list_or_empty.accept2(self)
            for type in type2:
                types.append(type.accept2(self))
            if len(type1[0]) == len(types):
                for x in xrange(0, len(type1[0])):
                    if type1[0][x] != types[x]:
                        if type1[0][x] == "float" and types[x] == "int":
                            return type1[1]
                        else:
                            self.isValid = False
                            self.errors.append("ERROR in line " + str(node.lineno) + ": Wrong arguments.")
                    else:
                        return type1[1]
            else:
                self.isValid = False
                self.errors.append("ERROR in line " + str(node.lineno) + ": Wrong number of arguments.")
        else:
            if len(type1[0]) > 0:
                self.isValid = False
                self.errors.append("ERROR in line " + str(node.lineno) + ": Wrong number of arguments.")
            return type1[1]

    def visit_ExpressionList(self, node):
        for ex in node.children:
            ex.Functions = node.Functions
            ex.Variables = node.Variables
        return node.children

    def visit_Fundefs(self, node):
        pass

    def visit_Fundefs_many(self, node):
        node.fundef.Functions = node.Functions
        node.fundef.Variables = node.Variables
        node.fundef.accept2(self)
        node.fundefs.Functions = node.Functions
        node.fundefs.Variables = node.Variables
        node.fundefs.accept2(self)

    def visit_Fundef(self, node):
        node.Functions.putNewFun(node.id, node.type)
        Functions = FunctionsTable(node.Functions, "Functions")
        Variables = SymbolTable(node.Variables, "Variables")
        if node.arg_list is not None:   # if arguments of functions exist
            node.arg_list.Functions = Functions
            node.arg_list.Variables = Variables
            listOfArguments = node.arg_list.accept2(self)
            for element in listOfArguments:
                if element is not None:
                    node.Functions.put(node.id, element.type)
                    if Variables.put(element.id, element.type) == -1:
                        self.errors.append("ERROR in line " + str(node.lineno) + ": Variable " + element.name + " has already been initialized in the current scope.")
        node.compound_instr.Functions = Functions
        node.compound_instr.Variables = Variables
        node.compound_instr.accept2(self)

    def visit_ArgumentList(self, node):
        for arg in node.children:
            arg.Functions = node.Functions
            arg.Variables = node.Variables
        return node.children

    def visit_Arg(self, node):
        return node.id, node.type
