# coding=utf-8
import logging

from pyage.core import address
from pyage.core.agent.aggregate import AggregateAgent
from pyage.core.emas import EmasService
from pyage.core.locator import GridLocator
from pyage.core.migration import ParentMigration
from pyage.core.statistics import TimeStatistics
from pyage.core.stop_condition import StepLimitStopCondition
from pyage.elect.el_crossover import Crossover
from pyage.elect.el_eval import  ClausulesEvaluator
from pyage.elect.el_init import EmasInitializer, root_agents_factory, ClausulesInitializer
from pyage.elect.el_mutation import Mutation
from pyage.elect.naming_service import NamingService

logger = logging.getLogger(__name__)

clausules_nr = 100
max_clausule_length = 3
number_of_variables = 10
clausules = ClausulesInitializer(clausules_nr, max_clausule_length, number_of_variables, 0)()
logger.info("Initial clausules:\n%s", "\n".join(map(str,clausules)))


agents_count = 4
logger.debug("EMAS, %s agents", agents_count)
agents = root_agents_factory(agents_count, AggregateAgent)

stop_condition = lambda: StepLimitStopCondition(100)

agg_size = 1000
aggregated_agents = EmasInitializer(clausule=clausules, size=agg_size, energy=40 )


emas = EmasService

minimal_energy = lambda: 20
reproduction_minimum = lambda: 110
migration_minimum = lambda: 130
newborn_energy = lambda: 100
transferred_energy = lambda: 30


evaluation = lambda: ClausulesEvaluator()
crossover = lambda: Crossover(size=30)
mutation = lambda: Mutation(probability=0.5, evol_probability=0.7)


address_provider = address.SequenceAddressProvider

migration = ParentMigration
locator = GridLocator


stats = TimeStatistics
naming_service = lambda: NamingService(starting_number=2)