import random
import time
from pyage.core.operator import Operator
from pyage.elect.el_genotype import Clausules

import logging

logger = logging.getLogger(__name__)


class ClausulesEvaluator(Operator):
    def __init__(self):
        super(ClausulesEvaluator, self).__init__(Clausules)

    def process(self, population):
        for genotype in population:
            genotype.fitness = self.evaluate(genotype)

    def evaluate(self, genotype):
        sums = 0
        len_sum = 0
        for clausule in genotype:

            y = sum([x[0].value if x[1] else 1-x[0].value for x in clausule])
            if y > 0:
                sums += 1
            len_sum +=1

        evalu = float((sums)/float(len_sum))**2
        # if evalu < 95:
        #     evalu -= random.randint(0,15)
        #     print evalu
        return evalu

    # class kApprovalEvaluator(Operator):

# def __init__(self, k, price_func, budget, initial_vote_places, candidate=1, type=None):
# 		super(kApprovalEvaluator, self).__init__(Votes)
# 		self.k = k
# 		self.price_func = price_func
# 		self.budget = budget
# 		self.candidate = candidate
# 		self.initial_vote_places = initial_vote_places
#
# 	def process(self, population):
# 		for genotype in population:
# 			genotype.fitness = self.evaluate(genotype)
#
# 	def evaluate(self, genotype):
# 		counter = 0
# 		points_list = []
# 		cash_sum = 0
# 		for vote in genotype.votes:
# 			new_index = vote.index(self.candidate)
# 			bias = new_index-self.initial_vote_places[counter]
# 			cash_sum += self.price_func[counter](bias)
# 			points_list += vote[:self.k]
# 			counter +=1
#
# 		points = dict((x, points_list.count(x)) for x in points_list)
# 		sorted_points = sorted(points.items(), key=lambda (a,b):b, reverse=True)
# 		_,max_val = sorted_points[0]
#
# 		all_max = [(a,b) for (a,b) in sorted_points if b==max_val]
#
# 		evaluated = None
# 		for (cand, points) in all_max:
# 			if cand == self.candidate and len(all_max)==1:
# 				evaluated = self.budget-cash_sum
# 				break
# 		if evaluated is None:
# 			randy = random.randint(0,50)
# 			evaluated = -9999999 + randy
# 		return evaluated
