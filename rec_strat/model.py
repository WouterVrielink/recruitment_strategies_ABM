import numpy as np

from mesa import Model
from mesa.time import RandomActivation
from mesa.space import MultiGrid

from ant import Ant

class Environment(Model):
    """ A model which contains a number of ant colonies. """
    def __init__(self, N=100, g=10, w=10, h=10, p_uf=1, p_ul=1, p_up=1, p_fl=1, role_division = (100,0,5,5), moore=False):
        """

        :param g: amount of ants possible in a following group of ants
        :param width: int, width of the system
        :param height: int, height of the system
        :param role_division: tuple with (nr_unassigned, nr_leaders, nr_followers, nr_pheromoners)
        :param moore: boolean, True/False whether Moore/vonNeumann is used
        """
        super().__init__()

        # Environment variables
        self.width = w
        self.height = h
        self.moore = moore
        self.grid = MultiGrid(w, h, False)

        # Environment attributes
        self.schedule = RandomActivation(self)

        # Ant variables
        self.g = g
        self.role_division = role_division
        self.N = np.sum(role_division) # give amount of ants a variable N
        for i, number in enumerate(role_division):
            self.add_ants(number, i)

    def get_random_position(self):
        """docstring for random position.""" #TODO
        return (np.random.randint(0, self.width), np.random.randint(0, self.height))

    def add_ants(self, N, role):
        """
        Adds N ants to this colony.
        :param N: integer value which specifies the nr of ants to add
        """
        for i in range(N):
            a = Ant(i, model=self, pos=None, role=role)
            # print(a.pos)
            self.grid.place_agent(a, a.pos)
            self.schedule.add(a)

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
                "is too large, pos_food {}".format(ant.pos, pos, self.food.get_food_pos())

        self.grid.move_agent(ant, pos)

    def step(self):
        """
        Do a single time-step using freeze-dry states, colonies are updated each time-step in random orders, and ants
        are updated per colony in random order.
        """
        self.schedule.step()

    def animate(self, ax):
        """

        :param ax:
        :return:
        """
        self.ax = ax
        self.animate_ants()

    def animate_ants(self):
        """
        Update the visualization part of the Ants.
        """
        for ant in self.schedule.agents:
            ant.update_vis()

    def grid_to_array(self, pos):
        """
        Convert the position/indices on self.grid to imshow array.
        :param pos: tuple (int: x, int: y)
        :return: tuple (float: x, float: y)
        """
        return pos[0], self.height - pos[1] - 1
