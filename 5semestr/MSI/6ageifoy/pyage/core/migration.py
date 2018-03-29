import logging
import random
import Pyro4
from pyage.core.agent.agent import AGENT
from pyage.core.inject import Inject

logger = logging.getLogger(__name__)

class Migration(object):
    def migrate(self, agent):
        raise NotImplementedError()


class Pyro4Migration(Migration):
    @Inject("ns_hostname")
    def __init__(self, probability = 0.05):
        super(Pyro4Migration, self).__init__()
        self.probability = probability

    def migrate(self, agent):
        try:
            if random.random() < self.probability and len(agent.parent.get_agents()) > 1:
                logger.debug("migrating!")
                aggregate = self._get_random_aggregate(agent)
                parent = agent.parent
                logger.debug("ADDING TO: " + str(aggregate))
                logger.debug("PARENT B FROM:" +str( len(parent.get_agents())))
                logger.debug("PARENT B TO:" + str(len(aggregate.get_agents())))
                aggregate.add_agent(agent.parent.remove_agent(agent))
                logger.debug("PARENT A FROM:" + str(len(parent.get_agents())))
                logger.debug("PARENT A TO:" + str(len(aggregate.get_agents())))
                return True
        except:
            logging.exception("")
        return False

    def _get_random_aggregate(self, agent):
        ns = Pyro4.locateNS(self.ns_hostname)
        agents = ns.list(AGENT)
        #logger.debug(agents)
        del agents[AGENT + "." + agent.parent.address]
        return Pyro4.Proxy(random.choice(agents.values()))


class ParentMigration(Migration):
    def migrate(self, agent):
        try:
            if random.random() > 0.95 and len(agent.parent.get_agents()) > 1 and len(
                agent.parent.parent.get_agents()) > 1:
                logger.debug("migrating!")
                aggregate = self.__get_random_aggregate(agent)
                old_parent = agent.parent
                aggregate.add_agent(agent.parent.remove_agent(agent))
                logger.debug("%s MIGRATED FROM PARENT %s to %s", agent, old_parent, aggregate)
                return True
        except:
            logging.exception("")
        return False

    def __get_random_aggregate(self, agent):
        siblings = list(agent.parent.parent.get_agents())
        return random.choice(siblings)


class NoMigration(Migration):
    def migrate(self, agent):
        pass
