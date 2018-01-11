import numpy as np

from mesa import Agent


class Ant(Agent):
    """An agent with fixed legs."""

    def __init__(self, unique_id, colony):
        super().__init__(unique_id, colony.environment)
        self.pos = colony.location
        self.environment = colony.environment
        self.colony = colony
        self.pheromone_id = colony.pheromone_id
        self.last_pos = (-1, -1)
        self.history = [colony.location]
        self.environment.grid.place_agent(self, self.pos)
        self.carry_food = False

    def step(self):
        positions, pheromone_levels = self.environment.get_pheromones(self.pos, self.pheromone_id)

        self.last_pos = self.pos
        self.pos = self.move(positions, pheromone_levels)

        if self.carry_food:
            self.environment.place_pheromones(self.pos)
        if [*self.pos] in np.array(np.where(self.environment.food.grid > 0)).T.tolist():
            self.carry_food = True
            print(self.history)
        if [*self.pos] == [*self.colony.pos]:
            self.carry_food = False
            self.history = []

        if not self.carry_food:
            self.history.append(self.pos)

    def move(self, positions, pheromone_levels):
        if self.carry_food:
            move_to = self.history.pop()
            print(move_to)
        else:
            norm = sum(pheromone_levels)
            l = len(pheromone_levels)
            if norm > 0:
                probabilities = pheromone_levels / sum(pheromone_levels)
            else:
                probabilities = np.ones(l) / l

            move_to = positions[np.random.choice(np.arange(len(positions)), p=probabilities)]

        self.environment.move_agent(self, move_to)

        return move_to
