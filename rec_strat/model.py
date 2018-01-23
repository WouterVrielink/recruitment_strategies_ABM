from mesa import Model
from mesa.time import RandomActivation
from mesa.space import MultiGrid
from mesa.datacollection import DataCollector
import metrics
import numpy as np
import random
from scipy.ndimage import gaussian_filter
from scipy.spatial import distance
from ant import Ant

class Environment(Model):
    """ A model which contains a number of ant colonies. """
    def __init__(self, g, width, height, role_division = (100,0,5,5), moore=False):
        """

        :param g: amount of ants possible in a following group of ants
        :param width: int, width of the system
        :param height: int, height of the system
        :param role_division: tuple with (nr_unassigned, nr_leaders, nr_followers, nr_pheromoners)
        :param moore: boolean, True/False whether Moore/vonNeumann is used
        """
        super().__init__()

        # Environment variables
        self.width = width
        self.height = height
        self.moore = moore
        self.grid = MultiGrid(width, height, False)

        # Environment attributes
        self.schedule = RandomActivation(self)

        # Ant variables
        self.g = g
        self.role_division = role_division
        self.N = np.sum(role_division) # give amount of ants a variable N

    def get_random_position(self):
        """docstring for random position.""" #TODO
        return (np.random.randint(0, self.width), np.random.randint(0, self.height))

    def add_ants(self, N, role):
        """
        Adds N ants to this colony.
        :param N: integer value which specifies the nr of ants to add
        """
        for i in range(N):
            a = Ant(i, self, role)
            self.environment.grid.place_agent(a, a.pos)
            self.environment.schedule.add(a)

        if N == 1:
            return a

    def move_agent(self, ant, pos):
        """
        Move an agent across the map.
        :param ant: class Ant
        :param pos: tuple (x, y)
        """
        if self.moore:
            assert np.sum(np.subtract(pos, ant.pos) ** 2) in [1, 2], \
                "the ant can't move from its original position {} to the new position {}, because the distance " \
                "is too large".format(ant.pos, pos)
        else:
            assert np.sum(np.subtract(pos, ant.pos) ** 2) == 1, \
                "the ant can't move from its original position {} to the new position {}, because the distance " \
                "is too large, loc_food {}".format(ant.pos, pos, self.food.get_food_pos())

        self.grid.move_agent(ant, pos)

    def step(self):
        """
        Do a single time-step using freeze-dry states, colonies are updated each time-step in random orders, and ants
        are updated per colony in random order.
        """
        self.schedule.step()