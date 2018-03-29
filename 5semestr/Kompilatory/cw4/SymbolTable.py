

class SymbolTable(object):

    def __init__(self, parent, name):
        self.parentScope = None
        if parent is not None:
            self.parentScope = parent
        self.dictionary = {}

    def put(self, name, symbol):
        if name in self.dictionary.keys():
            self.dictionary[name] = symbol
            return -1
        else:
            self.dictionary[name] = symbol
            return 0

    def get(self, name):
        if name in self.dictionary.keys():
            return self.dictionary[name]
        elif self.parentScope is not None:
            return self.getParentScope().get(name)
        else:
            return -1

    def getParentScope(self):
        return self.parentScope


class FunctionsTable(object):
    def __init__(self, parent, name):
        self.parentScope = None
        if parent is not None:
            self.parentScope = parent
        self.dictionary = {}
        self.returnType = {}

    def putNewFun(self, name, type):
        if name in self.dictionary.keys():
            self.dictionary[name] = []
            self.returnType[name] = type
            return -1
        else:
            self.dictionary[name] = []
            self.returnType[name] = type
            return 0

    def put(self, name, symbol):
        if name in self.dictionary.keys():
            self.dictionary[name].append(symbol)

    def get(self, name):
        if self.parentScope is not None:
            return self.getParentScope().get(name)
        elif name in self.dictionary.keys():
            return self.dictionary[name], self.returnType[name]
        else:
            return -1

    def getParentScope(self):
        return self.parentScope
