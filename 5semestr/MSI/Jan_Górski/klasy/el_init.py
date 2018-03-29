import random
from copy import deepcopy

from pyage.core.emas import EmasAgent
from pyage.core.operator import Operator
from pyage.elect.el_genotype import Clausules, LogicalVariable
from pyage.core.inject import Inject
import random


class EmasInitializer(object):
    def __init__(self, clausule, energy, size):
        self.clausule = clausule
        self.energy = energy
        self.size = size

    @Inject("naming_service")
    def __call__(self):
        agents = {}
        for i in range(self.size):
            agent = EmasAgent(Clausules(deepcopy(self.clausule)), self.energy, self.naming_service.get_next_agent())
            agents[agent.get_address()] = agent
        return agents


def root_agents_factory(count, type):
    def factory():
        agents = {}
        for i in range(count):
            agent = type('R' + str(i))
            agents[agent.get_address()] = agent
        return agents

    return factory


class ClausulesInitializer(object):
    def __init__(self, clausules_numeber, clausules_size, variable_number, seed):
        self.clausules_numeber = clausules_numeber
        self.clausules_size = clausules_size
        random.seed(seed)
        self.variable_number = variable_number

    def __call__(self):
        clausules_list = []
        variables = [LogicalVariable(random.randint(0,1),"Variable: " +str(x)) for x in xrange(self.variable_number)]
        new_var = set()
        DoneAll = False
        while not DoneAll:
            for x in xrange(self.clausules_numeber):
                var = random.sample(variables, self.clausules_size)
                new_var |= set(var)
                z = (list(zip(var, [random.randint(0, 1) for y in xrange(len(var))])))
                clausules_list.append([list(t) for t in z])
            if len(new_var) != len(variables):
                new_var = set()
                clausules_list = []
            else:
                DoneAll = True
        random.seed()

        return clausules_list

class EvolutionInitializer(Operator):
    def __init__(self, size, clausules):
        super(EvolutionInitializer, self).__init__(Clausules)
        self.size = size
        self.clausules = clausules

    def process(self, population):
        for i in range(self.size):
            population.append(Clausules(deepcopy(self.clausules)))
                    # print population
# class EmasInitializer(object):
#
#     def __init__(self,votes,candidate, energy, size):
#         self.votes = votes
#         self.candidate = candidate
#         self.energy = energy
#         self.size = size
#
#     @Inject("naming_service")
#     def __call__(self):
#         agents = {}
#         for i in range(self.size):
#             agent = EmasAgent(Votes(self.votes, self.candidate), self.energy, self.naming_service.get_next_agent())
#             agents[agent.get_address()] = agent
#         return agents
#
#
#
# def root_agents_factory(count, type):
#     def factory():
#         agents = {}
#         for i in range(count):
#             agent = type('R' + str(i))
#             agents[agent.get_address()] = agent
#         return agents
#
#     return factory
#
# class VotesInitializer(object):
#
#     def __init__(self, candidates_nr, voters_nr, c_nr, seed):
#         self.candidates_nr = candidates_nr
#         self.voters_nr = voters_nr
#         random.seed(seed)
#         self.c_nr = c_nr
#
#     def __call__(self):
#         basis = range(1,self.candidates_nr+1)
#         votes_list = [(random.shuffle(basis), list(basis))[1] for _ in xrange(self.voters_nr)]
#         c_places_list = [vote.index(self.c_nr) for vote in votes_list]
#         random.seed()
#         return votes_list, c_places_list