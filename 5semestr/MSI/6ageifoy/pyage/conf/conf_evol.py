# coding=utf-8
import logging

from pyage.core import address
from pyage.core.agent.agent import generate_agents, Agent
from pyage.core.locator import GridLocator
from pyage.core.migration import ParentMigration
from pyage.core.statistics import TimeStatistics
from pyage.core.stop_condition import StepLimitStopCondition
from pyage.elect.el_crossover import Crossover
from pyage.elect.el_eval import  ClausulesEvaluator
from pyage.elect.el_init import ClausulesInitializer, EvolutionInitializer
from pyage.elect.el_mutation import Mutation
from pyage.elect.el_selection import TournamentSelection
from pyage.elect.naming_service import NamingService

logger = logging.getLogger(__name__)

clausules_nr = 100
max_clausule_length = 3
number_of_variables = 10
clausules = ClausulesInitializer(clausules_nr, max_clausule_length, number_of_variables, 0)()
logger.info("Initial clausules:\n%s", "\n".join(map(str,clausules)))


agents_count = 4
logger.debug("EMAS, %s agents", agents_count)
agents = generate_agents("agent", agents_count, Agent)


stop_condition = lambda: StepLimitStopCondition(100)

agg_size = 1000


operators = lambda: [ClausulesEvaluator(), TournamentSelection(size=130, tournament_size=130),
                     Crossover(size=30),Mutation(probability=0.5, evol_probability=0.7)]

initializer = lambda: EvolutionInitializer(agg_size, clausules)

address_provider = address.SequenceAddressProvider

migration = ParentMigration
locator = GridLocator


stats = TimeStatistics
naming_service = lambda: NamingService(starting_number=2)