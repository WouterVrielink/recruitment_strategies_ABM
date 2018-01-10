from mesa import Model
from mesa.space import MultiGrid
from colony import Colony
import numpy as np


class Environment(Model):
    def __init__(self, width, height, n_colonies, n_ants, moore=False):
        super().__init__()
        self.width = width
        self.height = height
        self.grid = MultiGrid(width, height, False)
        self.colonies = [Colony(n_ants) for _ in range(n_colonies)]
        self.pheromones = np.zeros((width, height))
        self.moore = moore
        self.pheromone_level = 1
        self.food = []

    def step(self):
        for col in self.colonies:
            col.step()
        self.update_pheromones()

    def move_agent(self, ant, loc):
        self.grid.move_agent(ant, loc)

    def add_food(self):
        x = np.random.randint(0, self.width - 1, 1)
        y = np.random.randint(0, self.height - 1, 1)
        self.food.append((x, y))

    def place_pheromones(self, loc):
        self.pheromones[loc] += self.pheromone_level

    def get_pheromones(self, loc, id):
        indices = self.grid.get_neighborhood(loc, self.moore)
        pheromones = [self.pheromones[x, y] for x, y in indices]
        tuples = [(loc, p) for loc, p in zip(indices, pheromones)]
        return tuples

    def update_pheromones(self):
        pass
