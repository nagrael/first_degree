import logging
import random
from pyage.core.operator import Operator
from pyage.elect.el_genotype import Clausules

logger = logging.getLogger(__name__)

class AbstractMutation(Operator):
    def __init__(self, type, probability):
        super(AbstractMutation, self).__init__()
        self.probability = probability

    def process(self, population):
        for genotype in population:
            if random.random() < self.probability:
                self.mutate(genotype)

class Mutation(AbstractMutation):
    def __init__(self, probability, evol_probability):
        super(Mutation, self).__init__(Clausules, evol_probability)
        self.probability = probability

    def mutate(self, genotype):
        logger.debug("Mutating genotype: {0}".format(genotype))
        for clausule in genotype.clausule:
            rand = random.random()
            cand = random.choice(clausule)
            if rand < self.probability:
                cand[0].value = 1 - cand[0].value
