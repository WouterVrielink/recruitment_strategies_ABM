from ant import Ant
import numpy as np


class FoodGrid:
    """ Class that keeps track of where food is in its own grid """
    def __init__(self, environment):
        self.environment = environment
        self.width = environment.width
        self.height = environment.height
        self.grid = np.zeros((self.width, self.height))

    def step(self):
        """

        :return:
        """
        if np.count_nonzero(self.grid) == 0:
            self.add_food()


    def add_food(self, xy=None):
        """

        :param xy:
        :return:
        """
        if not xy:
            x = np.random.randint(0, self.width - 1, 1)
            y = np.random.randint(0, self.height - 1, 1)
            xy = (x, y)
        self.grid[xy] += 5000000
    def get_food_pos(self):
        """
        returns a list of lists of all the x, y positions
        :return: [[x, y], [x, y], ...]
        """
        return np.array(np.where(self.environment.food.grid > 0)).T.tolist()
