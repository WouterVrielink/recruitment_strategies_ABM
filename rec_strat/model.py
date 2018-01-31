import numpy as np

from mesa import Model
from mesa.time import RandomActivation
from mesa.space import MultiGrid
from mesa.datacollection import DataCollector

from ant import Ant
from roles import Unassigned, Follower, Leader, Pheromone


class Environment(Model):
    """ A model which contains a number of ant colonies. """

    def __init__(self, N=100, g=2, w=10, h=10, p_uf=0.5, p_pu=0.1, p_up=0.5, p_fl=0.8, p_lu=0.05,
                 role_division={Unassigned: 10, Follower: 0, Leader: 5, Pheromone: 5},
                 moore=False, grow=False):
        """

        :param g: amount of ants possible in a following group of ants
        :param width: int, width of the system
        :param height: int, height of the system
        :param role_division: tuple with (nr_unassigned, nr_followers, nr_leaders, nr_pheromoners)
        :param moore: boolean, True/False whether Moore/vonNeumann is used
        """
        super().__init__()

        # Environment variables
        self.width = w
        self.height = h
        self.moore = moore
        self.grow = grow
        self.grid = MultiGrid(w, h, torus=True)
        self.interaction_probs = {Unassigned: (-1, None),
                                  Follower: (-1, None),
                                  Leader: (p_uf, Follower),
                                  Pheromone: (p_up, Pheromone),
                                  "success": (p_fl, Leader),
                                  "failure": (p_lu, Unassigned),
                                  "scent_lost": (p_pu, Unassigned)}
        self.ant_counter = 0

        # Environment attributes
        self.schedule = RandomActivation(self)

        # Ant variables
        self.g = g
        self.role_division = role_division
        self.N = np.sum(role_division)  # give amount of ants a variable N
        for role, number in role_division.items():
            self.add_ants(number, role)

        model_reporters = {"unassigned": lambda m: sum([1 if a.role == Unassigned else 0 for a in m.schedule.agents]),
                           "followers": lambda m: sum([1 if a.role == Follower else 0 for a in m.schedule.agents]),
                           "leaders": lambda m: sum([1 if a.role == Leader else 0 for a in m.schedule.agents]),
                           "pheromone": lambda m: sum([1 if a.role == Pheromone else 0 for a in m.schedule.agents])}
        self.dc = DataCollector(model_reporters=model_reporters)

    def get_torus_coordinates(self, x, y):
        return x % self.width, y % self.height

    def get_torus_neighborhood(self, pos, moore, radius=1, include_center=False):
        x, y = pos

        coordinates = set()

        for dy in range(-radius, radius + 1):
            for dx in range(-radius, radius + 1):
                if dx == 0 and dy == 0 and not include_center:
                    continue

                if not moore and abs(dx) + abs(dy) > radius:
                    continue

                px, py = x + dx, y + dy

                px, py = self.get_torus_coordinates(px, py)

                coords = (px, py)

                if coords not in coordinates:
                    coordinates.add(coords)
                    yield coords


    def get_random_position(self):
        """docstring for random position."""  # TODO
        return (np.random.randint(0, self.width), np.random.randint(0, self.height))

    def add_ants(self, N, role):
        """
        Adds N ants to this colony.
        :param N: integer value which specifies the nr of ants to add
        """

        for _ in range(N):
            a = Ant(self.ant_counter, model=self, pos=None, role=role)
            # print(a.pos)
            self.grid.place_agent(a, a.pos)
            self.schedule.add(a)


            self.ant_counter += 1

        if N == 1:
            return a

    def move_agent(self, ant, pos):
        """
        Move an agent across the map.
        :param ant: class Ant
        :param pos: tuple (x, y)
        """
        # if self.moore:
        #     assert np.sum(np.subtract(pos, ant.pos) ** 2) in [1, 2], \
        #         "the ant can't move from its original position {} to the new position {}, because the distance " \
        #         "is too large".format(ant.pos, pos)
        # else:
        #     assert np.sum(np.subtract(pos, ant.pos) ** 2) == 1, \
        #         "the ant can't move from its original position {} to the new position {}, because the distance " \
        #         "is too large, pos_food {}".format(ant.pos, pos, self.food.get_food_pos())

        self.grid.move_agent(ant, pos)

    def get_role_probabilities(self):

        roles_n = [sum([1 if a.role == Unassigned else 0 for a in self.schedule.agents]),
                           0,
                           sum([1 if a.role == Leader else 0 for a in self.schedule.agents]),
                           sum([1 if a.role == Pheromone else 0 for a in self.schedule.agents])]

        print(roles_n)

        return np.array(roles_n) / sum(roles_n)

    def step(self):
        """
        Do a single time-step using freeze-dry states, colonies are updated each time-step in random orders, and ants
        are updated per colony in random order.
        """
        self.schedule.step()
        self.dc.collect(self)

        if self.grow and self.schedule.steps % 10:
            role_probs = self.get_role_probabilities()

            # role = np.random.choice([Unassigned, Follower, Leader, Pheromone], p=role_probs)

            self.add_ants(10, Unassigned)


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
