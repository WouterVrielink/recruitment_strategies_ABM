import numpy as np


class Unassigned:
    def role_actions(self):
        neighbors = self.model.grid.get_neighbors(self.pos, include_center=True, radius=0, moore=self.model.moore)
        if len(neighbors):
            n = np.random.choice(neighbors)
            recruit_chance, new_role = self.model.recruit_probs[n.role]
            if np.random.uniform(0, 1, 1) < recruit_chance:
                self.role = new_role
                if n.role == Leader:
                    n.followers.append(self)


class Follower:
    def role_actions(self):
        pass


class Leader:
    def role_actions(self):
        e = np.random.choice(["succes", "failure"])
        event_chance, new_role = self.model.event_probs[e]

        if np.random.uniform(0, 1, 1) < event_chance:
            self.role = new_role
            for f in self.followers:
                f.role = new_role
            self.followers = []


class Pheromone:
    def role_actions(self):
        event_chance, new_role = self.model.event_probs["scent_lost"]
        if np.random.uniform(0, 1, 1) < event_chance:
            self.role = new_role
