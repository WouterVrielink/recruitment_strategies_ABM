import numpy as np

from mesa import Agent

class Ant(Agent):
    """An agent with fixed initial wealth."""
    def __init__(self, unique_id, colony):
        super().__init__(unique_id, colony)
        self.pos = self.model.location
        self.environment = self.model.environment
        self.pheromone_id = self.model.pheromone_id

        self.environment.grid.place_agent(self, self.pos)

    def step(self):
        positions, pheromone_levels = self.environment.get_pheromones(self.pos, self.pheromone_id)

        self.pos = self.move(positions, pheromone_levels)

        self.environment.place_pheromones(self.pos)

    def move(self, positions, pheromone_levels):
        probabilities = pheromone_levels/sum(pheromone_levels)
        move_to = positions[np.random.choice(np.arange(len(positions)), p=probabilities)]

        self.environment.move_agent(self, move_to)

        return move_to
