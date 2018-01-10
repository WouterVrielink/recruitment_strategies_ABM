import numpy as np

from mesa import Agent

class Ant(Agent):
    """An agent with fixed initial wealth."""
    def __init__(self, unique_id, colony):
        super().__init__(unique_id, colony)
        self.location = self.model.location
        self.environment = self.model.environment
        self.pheromone_id = self.model.pheromone_id

    def step(self):
        locations, probabilities = self.environment.get_pheromones(self.location, pheromone_id)

        self.location = self.move(locations, probabilities)

        self.environment.place_pheromones(self.location)

    def move(locations, probabilities):
        move_to = np.random.choice(env_pheromones, p=probabilities)

        self.environment.move_agent(self, move_to)

        return move_to
