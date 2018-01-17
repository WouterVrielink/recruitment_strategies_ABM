from mesa import Model
from mesa.time import RandomActivation
from mesa.space import MultiGrid
from colony import Colony
from obstacle import Obstacle
from food import FoodGrid
from mesa.datacollection import DataCollector
import metrics
import numpy as np
import random
from scipy.ndimage import gaussian_filter
from scipy.spatial import distance
from ant import Ant

class Environment(Model):
    """ A model which contains a number of ant colonies. """

    def __init__(self, width, height, n_colonies, n_ants, n_obstacles, decay=0.99, sigma=0.1, moore=False):
        """
        :param width: int, width of the system
        :param height: int, height of the system
        :param n_colonies: int, number of colonies
        :param n_ants: int, number of ants per colony
        :param decay: float, the rate in which the pheromone decays
        :param sigma: float, sigma of the Gaussian convolution
        :param moore: boolean, True/False whether Moore/vonNeumann is used
        """
        super().__init__()
        self.width = width
        self.height = height
        self.moore = moore

        self.grid = MultiGrid(width, height, False)
        self.schedule = RandomActivation(self)
        self.colonies = [Colony(self, i, (width // 2, height // 2), n_ants) for i in range(n_colonies)]
        self.pheromones = np.zeros((width, height), dtype=np.float)
        self.pheromone_level = 1
        self.food = FoodGrid(self)
        self.food.add_food()
        self.diff_kernel = np.array(
            [[0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 4, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0]])
        self.diff_kernel = self.diff_kernel / np.sum(self.diff_kernel) * decay
        self.sigma = sigma
        self.decay = decay
        self.pheromone_updates = []
        self.paths = []
        self.obstacles = []
        for _ in range(n_obstacles):
            self.obstacles.append(Obstacle(self))
        self.min_distance = distance.cityblock(self.colonies[0].pos, self.food.get_food_pos())
        self.datacollector = DataCollector(
            model_reporters={"Minimum path length": metrics.min_path_length,
                             "Mean minimum path length": metrics.mean_min_path_length},
            agent_reporters={"Agent minimum path length": lambda x: min(x.path_lengths),
                            "Encounters": Ant.count_encounters})

        # animation attributes
        self.pheromone_im = None
        self.ax = None

    def step(self):
        """
        Do a single time-step using freeze-dry states, colonies are updated each time-step in random orders, and ants
        are updated per colony in random order.
        """
        self.food.step()
        self.datacollector.collect(self)

        # Update all colonies
        for col in random.sample(self.colonies, len(self.colonies)):
            col.step()

        self.schedule.step()
        self.update_pheromones()

    def move_agent(self, ant, pos):
        """
        Move an agent across the map.
        :param ant: class Ant
        :param pos: tuple (x, y)
        """
        if self.moore:
            assert np.sum(np.subtract(pos, ant.pos) ** 2) in [1, 2], \
                "the ant can't move from its original position {} to the new position {}, because the distance " \
                "is too large".format(ant.pos, pos)
        else:
            assert np.sum(np.subtract(pos, ant.pos) ** 2) == 1, \
                "the ant can't move from its original position {} to the new position {}, because the distance " \
                "is too large".format(ant.pos, pos)
        self.grid.move_agent(ant, pos)

    def get_random_position(self):
        return (np.random.randint(0, self.width), np.random.randint(0, self.height))

    def position_taken(self, pos):
        if pos in self.food.get_food_pos():
            return True

        for colony in self.colonies:
            if colony.on_colony(pos):
                return True

        for obstacle in self.obstacles:
            if obstacle.on_obstacle(pos):
                return True

        return False

    def add_food(self):
        """
        Add food somewhere on the map, which is not occupied by a colony yet
        """
        self.food.add_food()

    def place_pheromones(self, pos):
        """
        Add pheromone somewhere on the map
        :param pos: tuple (x, y)
        """
        self.pheromone_updates.append((pos, self.pheromone_level))

    def get_neighbor_pheromones(self, pos, id):
        """
        Get the passable neighboring positions and their respective pheromone levels for the pheromone id
        :param pos:
        :param id:
        :return:
        """
        indices = self.grid.get_neighborhood(pos, self.moore)
        indices = [x for x in indices if not any([isinstance(x, Obstacle) for x in self.grid[x[0]][x[1]]])]
        pheromones = [self.pheromones[x, y] for x, y in indices]
        # tuples = [(loc, p) for loc, p in zip(indices, pheromones)]
        return indices, pheromones

    def update_pheromones(self):
        """
        Place the pheromones at the end of a timestep on the grid. This is necessary for freeze-dry time-steps
        """
        for (pos, level) in self.pheromone_updates:
            # self.pheromones[pos] += level
            self.pheromones[pos] += 1

        self.pheromone_updates = []

        # convolution by convolve 2d, uses self.diff_kernel
        # self.pheromones = signal.convolve2d(self.pheromones, self.diff_kernel, mode='same')

        # gaussian convolution using self.sigma
        self.pheromones = gaussian_filter(self.pheromones, self.sigma) * self.decay

        # self.pheromones = np.maximum(0.01, self.pheromones)

    def animate(self, ax):
        """

        :param ax:
        :return:
        """
        self.ax = ax
        self.animate_pheromones()
        self.animate_colonies()
        self.animate_ants()
        self.animate_food()
        self.animate_obstacles()

    def animate_pheromones(self):
        """
        Update the visualization part of the Pheromones.
        :param ax:
        """

        pheromones = np.rot90(self.pheromones.astype(np.float64).reshape(self.width, self.height))
        if not self.pheromone_im:
            self.pheromone_im = self.ax.imshow(pheromones,
                                               vmin=0, vmax=50,
                                               interpolation='None', cmap="Purples")
        else:
            self.pheromone_im.set_array(pheromones)

    def animate_colonies(self):
        """
        Update the visualization part of the Colonies.
        :return:
        """
        for colony in self.colonies:
            colony.update_vis()

    def animate_food(self):
        """
        Update the visualization part of the FoodGrid.
        :return:
        """
        self.food.update_vis()

    def animate_ants(self):
        """
        Update the visualization part of the Ants.
        """
        for ant in self.schedule.agents:
            ant.update_vis()

    def animate_obstacles(self):
        """
        Update the visualization part of the Obstacles.
        :return:
        """
        for obstacle in self.obstacles:
            obstacle.update_vis()

    def grid_to_array(self, pos):
        """
        Convert the position/indices on self.grid to imshow array.
        :param pos: tuple (int: x, int: y)
        :return: tuple (float: x, float: y)
        """
        return pos[0] - 0.5, self.height - pos[1] - 1.5
