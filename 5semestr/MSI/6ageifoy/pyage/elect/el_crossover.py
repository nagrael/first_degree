import random
from copy import deepcopy

from pyage.core.operator import Operator
from pyage.elect.el_genotype import Clausules

import logging

logger = logging.getLogger(__name__)
class AbstractCrossover(Operator):
    def __init__(self, type, size):
        super(AbstractCrossover, self).__init__(type)
        self.__size = size

    def process(self, population):
        parents = list(population)
        for i in range(len(population), self.__size):
            p1, p2 = random.sample(parents, 2)
            genotype = self.cross(p1, p2)
            population.append(genotype)

class Crossover(AbstractCrossover):
    def __init__(self, size):
        super(Crossover, self).__init__(Clausules, size)

    def cross(self, p1, p2):
        logger.debug("Crossing:\n{0}\nAND\n{1}".format(p1, p2))
        division = random.randint(1, len(p1) - 2)
        new_clausules = deepcopy(p1)
        for counter in xrange(division,len(p1)):
            for atom in xrange(len(new_clausules.clausule[counter])):
                new_clausules.clausule[counter][atom][0].value = p2.clausule[counter][atom][0].value

        logger.debug("new clausules:" + str(new_clausules))
        return new_clausules
