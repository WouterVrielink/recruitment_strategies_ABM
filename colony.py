from mesa.time import RandomActivation
from ant import Ant
from mesa import Agent
import numpy as np

class Colony(Agent):
    """ A Colony which contains a number of ants."""
    def __init__(self, environment, pheromone_id, pos, N, radius=1):
        self.environment = environment
        self.pheromone_id = pheromone_id
        self.pos = pos
        self.num_agents = N
        self.ant_list = RandomActivation(environment)
        self.radius = radius

        # Create agents
        self.add_ants(N)

        # register self
        self.environment.grid.place_agent(self, self.pos)

    def on_colony(self, pos):
        """
        Checks whether the pos is on top of its own colony.
        :param pos: tuple (x, y) coordinates
        :return: True if on colony, False otherwise
        """
        return np.sum(np.subtract(pos, self.pos) ** 2) ** 0.5 <= self.radius


    def step(self):
        '''
        Advance each ant in this colony by one time-step.
        '''
        self.ant_list.step()

    def add_ants(self, N):
        """
        Adds N ants to this colony.
        :param N: integer value which specifies the nr of ants to add
        """
        for i in range(N):
            a = Ant(i, self)
            self.ant_list.add(a)
