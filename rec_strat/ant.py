from mesa import Agent
import numpy as np
import random
import matplotlib.patches as patches
from roles import Unassigned, Follower, Leader, Pheromone
from copy import copy

role_colours = {Unassigned: 'g', Follower: 'r', Leader: 'b', Pheromone: 'c'}

class Ant(Agent):
    """docstring for Ant."""

    def __init__(self, id, model, pos=None, role=Unassigned):
        super(Ant, self).__init__(id, model)

        # Agent attributes
        self.model = model

        self._role = None
        self.role = role

        # Agent variables
        self.pos = pos if pos is not None else self.model.get_random_position()

        self.followers = []

        # Visualization
        self._patch = None
        self.size = 0.4

    @property
    def role(self):
        return self._role

    @role.setter
    def role(self, new_role):
        self._role = new_role

    def get_neighbors(self):
        x, y = self.pos

        neighbors = copy(self.model.grid.grid[x][y])

        neighbors.remove(self)

        return neighbors

    def step(self):
        self.move()

        self.role.role_actions(self)

    def move(self):
        possibilities = list(self.model.get_torus_neighborhood(self.pos, self.model.moore))

        self.model.move_agent(self, random.choice(possibilities))

    def update_vis(self):
        """
        :return:
        """
        pos = self.model.grid_to_array(self.pos)
        pos = (pos[0] + (1 - self.size) / 2, pos[1] + (1 - self.size) / 2)

        if not self._patch:
            self._patch = patches.Rectangle(pos, self.size, self.size, linewidth=2,
                                            edgecolor='k', facecolor='w', fill=True, zorder=2)
            self.model.ax.add_patch(self._patch)

        self._patch.set_facecolor(role_colours[self.role])
        self._patch.set_xy(pos)

        return self._patch
