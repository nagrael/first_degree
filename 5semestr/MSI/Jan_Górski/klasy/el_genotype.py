#
# class Votes(object):
#     def __init__(self, votes, candidate):
#         self.votes = [list(h) for h in votes]
#         self.fitness = None
#         self.candidate = candidate
#
#     def __str__(self):
#         return "{0}\nfitness: {1}".format("\n".join(map(str,self.votes)), self.fitness)
#


class LogicalVariable(object):
    def __init__(self, value, number):
        self.value = value
        self.number = number


    def __str__(self):
        return self.number + ": " + str(self.value)

class Clausules(object):
    def __init__(self, clausule):
        self.clausule = clausule
        self.fitness = None

    def __iter__(self):
        return iter(self.clausule)

    def __len__(self):
        return len(self.clausule)

    def __str__(self):
        names = list()
        for a in self.clausule:
            names.append("(")
            for b in a:
                if b[1]:
                    names.append([b[0].number, b[0].value])
                else:
                    names.append(["!" + b[0].number, b[0].value])
            names.append(")")
        return "{0}\nfitness: {1}".format("\n".join(map(str, names)), self.fitness)