import logging
import time
from pyage.core.statistics import Statistics
import os

logger = logging.getLogger(__name__)


class StepStatistics(Statistics):
    def __init__(self, output_file_name='fitness_pyage.txt'):
        self.history = []
        self.fitness_output = open(output_file_name, 'a')

    def __del__(self):
        self.fitness_output.close()

    def append(self, best_fitness, step_count):
        self.fitness_output.write(str(step_count - 1) + ';' + str(best_fitness) + '\n')
        self.fitness_output.flush()
        os.fsync(self.fitness_output)

    def update(self, step_count, agents):
        try:
            best_fitness = max([a.get_fitness() for a in agents])
            #print  max(agents, key=lambda a: a.get_fitness()).get_best_genotype()
            logger.debug(best_fitness)
            self.history.append(best_fitness)
            if (step_count - 1) % 100 == 0:
                self.append(best_fitness, step_count)
        except:
            logging.exception("")

    def summarize(self, agents):
        try:
            logger.debug(self.history)
            best_agent = max(agents, key=lambda a: a.get_fitness())
            best_genotype = best_agent.get_best_genotype()
            self.fitness_output.write("best genotype:\n%s" % best_genotype)
        except Exception as e:
            logging.exception(e)


class TimeStatistics(StepStatistics):
    def __init__(self, output_file_name='fitness_pyage.txt'):
        super(TimeStatistics, self).__init__(output_file_name)
        self.start = time.time()

    def append(self, best_fitness, step_count):
        self.fitness_output.write(str(time.time() - self.start) + ';' + str(best_fitness) + '\n')
