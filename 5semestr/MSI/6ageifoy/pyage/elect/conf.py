# coding=utf-8
import logging
import os
import math

from pyage.core import address

from pyage.core.agent.aggregate import AggregateAgent
from pyage.core.emas import EmasService
from pyage.core.locator import GridLocator
from pyage.core.migration import ParentMigration
from pyage.core.statistics import TimeStatistics
from pyage.core.stats.gnuplot import StepStatistics
from pyage.core.stop_condition import StepLimitStopCondition

from pyage.elect.el_crossover import Crossover
from pyage.elect.el_eval import kApprovalEvaluator, ClausulesEvaluator
from pyage.elect.el_init import EmasInitializer, root_agents_factory, ClausulesInitializer, EvolutionInitializer
from pyage.elect.el_mutation import Mutation
from pyage.elect.el_selection import TournamentSelection
from pyage.elect.naming_service import NamingService

logger = logging.getLogger(__name__)

clausules_numeber = 50
clausules_size = 3
variable_number = 15
clausules = ClausulesInitializer(clausules_numeber, clausules_size, variable_number, 0)()
logger.info("Initial votes:\n%s", "\n".join(map(str,clausules)))

agg_size = clausules_numeber*10


agents_count = 4
logger.debug("EMAS, %s agents", agents_count)
agents = root_agents_factory(agents_count, AggregateAgent)

stop_condition = lambda: StepLimitStopCondition(20000)

agg_size = 40
aggregated_agents = EmasInitializer(clausule=clausules, energy=40, size=agg_size )

emas = EmasService

minimal_energy = lambda: 80
reproduction_minimum = lambda: 110
migration_minimum = lambda: 130
newborn_energy = lambda: 100
transferred_energy = lambda: 25

# budget = 0
# evaluation = lambda: kApprovalEvaluator(k_approval_coeff,[simple_cost_func]*votes_nr,budget, init_c_places, chosen_candidate)
# crossover = lambda: Crossover(size=30)
# mutation = lambda: Mutation(probability=0.2, evol_probability=0.5)
evaluation = lambda: ClausulesEvaluator()
crossover = lambda: Crossover(size=30)
mutation = lambda: Mutation(probability=0.1, evol_probability=0.2)
def simple_cost_func(x): return abs(x)*10

#
# address_provider = address.SequenceAddressProvider
#
# migration = ParentMigration
# locator = GridLocator
#
# stats = lambda: StepStatistics('fitness_%s_pyage.txt' % __name__)
#
# naming_service = lambda: NamingService(starting_number=2)
# operators = lambda: [evaluation(), TournamentSelection(size=130, tournament_size=130), crossover(), mutation()]
#
# initializer = lambda: TheInitializer(agg_size,clausules)

address_provider = address.SequenceAddressProvider

migration = ParentMigration
locator = GridLocator

#stats = lambda: StepStatistics('fitness_%s_pyage.txt' % __name__)
stats = TimeStatistics
naming_service = lambda: NamingService(starting_number=2)