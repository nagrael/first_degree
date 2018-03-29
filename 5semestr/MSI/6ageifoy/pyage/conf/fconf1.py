# coding=utf-8
import logging
import os
import math

from pyage.core import address
from pyage.solutions.evolution.__init__ import TheInitializer

from pyage.core.agent.agent import *

from pyage.solutions.evolution.selection import TournamentSelection

import Pyro4
from pyage.core.migration import Pyro4Migration

from pyage.core.statistics import TimeStatistics

from pyage.core.agent.aggregate import AggregateAgent
from pyage.core.emas import EmasService
from pyage.core.locator import GridLocator
from pyage.core.migration import ParentMigration
from pyage.core.stats.gnuplot import StepStatistics
from pyage.core.stop_condition import StepLimitStopCondition

from pyage.solutions.evolution.crossover import Crossover
from pyage.solutions.evolution.eval import Evaluator 
from pyage.solutions.evolution.__init__ import EmasInitializer, root_agents_factory, ClausulesInitializer
from pyage.solutions.evolution.mutation import Mutation
from pyage.elect.naming_service import NamingService

logger = logging.getLogger(__name__)

clausules_nr = 100
max_clausule_length = 3
number_of_atoms = 10
clausules = ClausulesInitializer(clausules_nr, max_clausule_length, number_of_atoms, 0)()
logger.info("Initial clausules:\n%s", "\n".join(map(str,clausules)))


agents_count = 4
logger.debug("EMAS, %s agents", agents_count)
agents = generate_agents("agent", agents_count, Agent)
root_agents_factory(agents_count, AggregateAgent)

stop_condition = lambda: StepLimitStopCondition(1000)

agg_size = 1000
#aggregated_agents = EmasInitializer(votes=votes, candidate = chosen_candidate, size=agg_size, energy=40 )
aggregated_agents = EmasInitializer(clausules=clausules, size=agg_size, energy=40 )


emas = EmasService

minimal_energy = lambda: 80
reproduction_minimum = lambda: 110
migration_minimum = lambda: 130
newborn_energy = lambda: 100
transferred_energy = lambda: 25

#evaluation = lambda: kApprovalEvaluator(k_approval_coeff,[simple_cost_func]*votes_nr,budget, init_c_places, chosen_candidate)
#crossover = lambda: Crossover(size=30)
#mutation = lambda: Mutation(probability=0.2, evol_probability=0.5)
evaluation = lambda: Evaluator()
crossover = lambda: Crossover(size=30)
mutation = lambda: Mutation(probability=0.1, evol_probability=0.2)
#operators = lambda: [evaluation, TournamentSelection(size=125, tournament_size=125),
#                     crossover, mutation]
operators = lambda: [evaluation(), TournamentSelection(size=130, tournament_size=130), crossover(), mutation()]

initializer = lambda: TheInitializer(agg_size,clausules)

address_provider = address.SequenceAddressProvider

migration = ParentMigration
locator = GridLocator

#stats = lambda: StepStatistics('fitness_%s_pyage.txt' % __name__)
stats = TimeStatistics
naming_service = lambda: NamingService(starting_number=2)