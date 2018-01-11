from mesa import Model
from mesa.space import MultiGrid
from colony import Colony
from food import FoodGrid
import numpy as np
from scipy import signal
from scipy.ndimage import gaussian_filter


class Environment(Model):
    def __init__(self, width, height, n_colonies, n_ants, decay=0.2, sigma=0.1, moore=False):
        super().__init__()
        self.width = width
        self.height = height
        self.grid = MultiGrid(width, height, False)
        self.colonies = [Colony(self, i, (width//2, height//2), n_ants) for i in range(n_colonies)]
        self.pheromones = np.zeros((width, height), dtype=np.float)
        self.moore = moore
        self.pheromone_level = 1
        self.food = Food(self)
        self.food.add_food()
        self.diff_kernel = np.array(
            [[0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 4, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0]])
        self.diff_kernel = self.diff_kernel / np.sum(self.diff_kernel) * decay
        self.sigma = sigma
        self.decay = decay
        self.pheromone_updates = []
        self.path_lengths = []
        self.min_path_lengths = []

    def step(self):
        for col in self.colonies:
            col.step()
        self.update_pheromones()
        self.food.step()
        if len(self.path_lengths) > 0:
            self.min_path_lengths.append(min(self.path_lengths))
        else:
            self.min_path_lengths.append(None)
    def move_agent(self, ant, loc):
        self.grid.move_agent(ant, loc)

    def add_food(self):
        self.food.add_food()

    def place_pheromones(self, loc):
        self.pheromone_updates.append((loc, self.pheromone_level))

    def get_pheromones(self, loc, id):
        indices = self.grid.get_neighborhood(loc, self.moore)
        pheromones = [self.pheromones[x, y] for x, y in indices]
        # tuples = [(loc, p) for loc, p in zip(indices, pheromones)]
        return indices, pheromones

    def update_pheromones(self):
        for (loc, level) in self.pheromone_updates:
            # self.pheromones[loc] += level
            self.pheromones[loc] += 1

        self.pheromone_updates = []

        # convolution by convolve 2d, uses self.diff_kernel
        # self.pheromones = signal.convolve2d(self.pheromones, self.diff_kernel, mode='same')

        # gaussian convolution using self.sigma
        self.pheromones = gaussian_filter(self.pheromones, self.sigma) * self.decay

        # self.pheromones = np.maximum(0.01, self.pheromones)
