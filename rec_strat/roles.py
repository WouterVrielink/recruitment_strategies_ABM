import numpy as np
import random

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
                if np.random.random() < transition_chance:
                    for follower in self.followers:
                        follower.role = new_role
                    self.followers = []
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
                if np.random.uniform(0, 1, 1) < event_chance:
                    self.role = new_role
