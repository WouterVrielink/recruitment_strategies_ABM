from mesa import Agent
from mesa.time import RandomActivation

from ant import Ant

class Colony(Model):
    """A model with some number of agents."""
    def __init__(self, environment, pheromone_id, location, N):
        self.environment = Environment
        self.pheromone_id = pheromone_id
        self.location = location
        self.num_agents = N
        self.ant_list = RandomActivation(self)

        # Create agents
        self.add_ants(N)

    def step(self):
        '''Advance the model by one step.'''
        self.ant_list.step()

    def add_ants(N):
        for i in range(N):
            a = Ant(i, self)
            self.ant_list.add(a)
