# -*- coding: utf-8 -*-
"""
Roles module. These objects can be used to specify roles for agents.

Note:
    When implementing new 'roles' keep in mind that 'self' is actually the Ant
    agent that was passed when calling the method.

Core Objects:
    Role: Base class. Raises NotImplementedError if methods are not overloaded.
    Unassigned: Has no current role. When meeting a Leader, has a chance to
        become a follower of that leader. When meeting a Pheromone, has a chance
        to become a Pheromone.
    Follower: Follows a leader. Has no special actions.
    Leader: Leads a group of Followers.
    Pheromone: Pheromones
"""
import random
import numpy as np

class Role:
    @property
    def visualization_color(self):
        raise NotImplementedError

    def role_actions(self):
        raise NotImplementedError

class Unassigned(Role):
    @property
    def visualization_color(self):
        return 'g'

    def role_actions(self):
        neighbors = self.get_neighbors()

        if neighbors:
            n = random.choice(list(neighbors))

            transition_chance, new_role = self.model.interaction_probs[n.role]

            if np.random.random() < transition_chance:
                if n.role == Leader and len(n.followers) < self.model.g:
                    n.followers.append(self)
                    self.role = new_role
                elif n.role == Pheromone:
                    self.role = new_role

class Follower(Role):
    @property
    def visualization_color(self):
        return 'r'

    def role_actions(self):
        pass

class Leader(Role):
    @property
    def visualization_color(self):
        return 'b'

    def role_actions(self):
        neighbors = self.get_neighbors()

        if neighbors:
            n = random.choice(list(neighbors))

            if n in self.followers:
                transition_chance, new_role = self.model.interaction_probs["success"]
            else:
                transition_chance, new_role = self.model.interaction_probs["failure"]

            if np.random.random() < transition_chance:
                for follower in self.followers:
                    follower.role = new_role

                self.role = new_role
                self.followers = []

class Pheromone(Role):
    @property
    def visualization_color(self):
        return 'c'

    def role_actions(self):
        neighbors = self.get_neighbors()

        if neighbors:
            n = random.choice(list(neighbors))
            if n.role != self.role:
                event_chance, new_role = self.model.interaction_probs["scent_lost"]
                if np.random.random() < event_chance:
                    self.role = new_role
