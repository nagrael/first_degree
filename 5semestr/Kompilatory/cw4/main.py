#!C:\Python27\python.exe -u

import sys
import ply.yacc as yacc
from Cparser import Cparser
from TypeChecker import TypeChecker
from Interpreter import Interpreter

if __name__ == '__main__':
    sys.setrecursionlimit(10000)

    try:
        filename = sys.argv[1] if len(sys.argv) > 1 else "tests/loops.in"
        file = open(filename, "r")
    except IOError:
        print("Cannot open {0} file".format(filename))
        sys.exit(0)

    Cparser = Cparser()
    parser = yacc.yacc(module=Cparser)
    text = file.read()
    ast = parser.parse(text, lexer=Cparser.scanner)
    typeChecker = TypeChecker()
    #print ast
    for str in ast.accept2(typeChecker):
        pass
         #print str

    if typeChecker.isValid:
     #   print " "
      #  print "Interpretacion: "
        ast.accept(Interpreter())
    else:
        print "ERRORS FOUND"


