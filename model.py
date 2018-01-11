from mesa import Model
from mesa.space import MultiGrid
from colony import Colony
from food import Food
import numpy as np
from scipy import signal


class Environment(Model):
    def __init__(self, width, height, n_colonies, n_ants, decay=0.9, moore=False):
        super().__init__()
        self.width = width
        self.height = height
        self.grid = MultiGrid(width, height, False)
        self.colonies = [Colony(self, i, (1, 1), n_ants) for i in range(n_colonies)]
        self.pheromones = np.zeros((width, height))
        self.moore = moore
        self.pheromone_level = 1
        self.food = Food(self)
        self.food.add_food()
        self.diff_kernel = np.array(
            [[0, 0, 1, 0, 0], [0, 1, 2, 1, 0], [1, 2, 4, 2, 1], [0, 1, 2, 1, 0], [0, 0, 1, 0, 0]])
        self.diff_kernel = self.diff_kernel / np.sum(self.diff_kernel) * decay

    def step(self):
        for col in self.colonies:
            col.step()
        self.update_pheromones()
        self.food.step()

    def move_agent(self, ant, loc):
        self.grid.move_agent(ant, loc)

    def add_food(self):
        self.food.add_food()

    def place_pheromones(self, loc):
        self.pheromones[loc] += self.pheromone_level

    def get_pheromones(self, loc, id):
        indices = self.grid.get_neighborhood(loc, self.moore)
        pheromones = [self.pheromones[x, y] for x, y in indices]
        # tuples = [(loc, p) for loc, p in zip(indices, pheromones)]
        return indices, pheromones

    def update_pheromones(self):
        pheromones = signal.convolve2d(self.pheromones, self.diff_kernel,mode='same')
        self.pheromones = pheromones[0:self.width, 0:self.height]
