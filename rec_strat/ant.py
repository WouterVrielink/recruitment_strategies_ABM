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
        self.role_funcs = [self.get_new_role_u, self.get_new_role_f, self.get_new_role_l, self.get_new_role_p]

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
        self.get_new_role = self.role_funcs[new_role]

    @profile
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

    @profile
    def move(self):
        posibilities = list(self.model.get_torus_neighborhood(self.pos, self.model.moore))

        self.model.move_agent(self, random.choice(posibilities))

    def get_new_role_u(self):
        neighbors = self.model.grid.get_neighbors(self.pos, include_center=True, radius=0, moore=self.model.moore)
        if len(neighbors):
            n = np.random.choice(neighbors)
            if n.role > 1:
                if np.random.uniform(0, 1, 1) < self.model.transition_p[n.role][0]:
                    self.role = self.model.transition_p[n.role][1]
                    if n.role == 2:
                        n.followers.append(self)

    def get_new_role_f(self):
        pass

    def get_new_role_l(self):
        c = np.random.choice([4, 6])
        if np.random.uniform(0, 1, 1) < self.model.transition_p[c][0]:
            self.role = self.model.transition_p[c][1]
            for f in self.followers:
                f.role = self.model.transition_p[c][1]
            self.followers = []

    def get_new_role_p(self):
        if np.random.uniform(0, 1, 1) < self.model.transition_p[5][0]:
            self.role = 0

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
