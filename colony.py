from mesa import Model
from mesa.time import RandomActivation

from ant import Ant

class Colony(Model):
    """A model with some number of agents."""
    def __init__(self, N):
        self.num_agents = N
        self.ant_list = RandomActivation(self)

        # Create agents
        for i in range(self.num_agents):
            a = Ant(i, self)
            self.ant_list.add(a)

        # TODO environment

    def step(self):
        '''Advance the model by one step.'''
        self.ant_list.step()
