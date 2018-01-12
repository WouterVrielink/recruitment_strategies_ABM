import numpy as np


class FoodGrid:
    """ Class that keeps track of where food is in its own grid. """
    def __init__(self, environment):
        self.environment = environment
        self.width = environment.width
        self.height = environment.height
        self.grid = np.zeros((self.width, self.height))

    def step(self):
        """
        When there is no more food left on the map, add one food location.
        """
        if np.count_nonzero(self.grid) == 0:
            self.add_food()

    def add_food(self, xy=None):
        """
        Adds food on the position specified by xy. If no xy is specified a random location is seleced that is not on a
        colony.
        :param xy: a tuple of integers (x, y)
        """
        while not xy:
            x = np.random.randint(0, self.width, 1)[0]
            y = np.random.randint(0, self.height, 1)[0]
            if not any([colony.on_colony((x, y)) for colony in self.environment.colonies]):
                xy = (x, y)
        self.grid[xy] += 5000000

    def get_food_pos(self):
        """
        Returns a list of tuples of all the x, y positions
        :return: [(x, y), (x, y), ...]
        """
        return [(x, y) for x, y in np.array(np.where(self.grid > 0)).T.tolist()]
