from mesa import Agent
import numpy as np
import random
import matplotlib.patches as patches

role_colours = ['g', 'r', 'b', 'c']


class Ant(Agent):
    """docstring for Ant."""

    def __init__(self, id, model, pos=None, role=0):
        super(Ant, self).__init__(id, model)

        # Agent attributes
        self.model = model
        self.role = role

        # Agent variables
        self.pos = pos if pos is not None else self.model.get_random_position()

        self.followers = []

        # Visualization
        self._patch = None
        self.size = 0.4

    def step(self):
        self.move()

        self.get_new_role()

        # self.role_actions()

    def role_actions(self):
        raise NotImplementedError

        # Follower
        if self.role == 1:
            pass
        # Leader
        elif self.role == 2:
            pass
        # Pheromone
        elif self.role == 3:
            pass

    def move(self):
        posibilities = self.model.grid.get_neighborhood(self.pos, moore=self.model.moore)

        self.model.move_agent(self, random.choice(posibilities))

    def get_new_role(self):
        if self.role == 0:
            neighbors = self.model.grid.get_neighbors(self.pos, include_center=True, radius=0,
                                                      moore=self.model.moore)
            if len(neighbors):
                n = np.random.choice(neighbors)
                if n.role > 1:
                    if np.random.uniform(0, 1, 1) < self.model.transition_p[n.role][0]:
                        self.role = self.model.transition_p[n.role][1]
        elif self.role == 1:
            pass
        elif self.role == 2:
            if np.random.uniform(0, 1, 1) < self.model.transition_p[4][0]:
                for f in self.followers:
                    f.role = 2
                self.followers = []
        elif self.role == 3:
            if np.random.uniform(0, 1, 1) < self.model.transition_p[5][0]:
                self.role = 0

    def _role_count(self, agents, role):
        return sum([1 if a.role == role else 0 for a in agents])

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
