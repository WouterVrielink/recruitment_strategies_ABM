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
        """
        Do a single time-step. Function called by colony
        """
        # get the possible positions to move too, and their respective pheromone levels
        positions, pheromone_levels = self.environment.get_pheromones(self.pos, self.pheromone_id)

        # store current position and move to the next
        self.last_pos = self.pos
        self.move(positions, pheromone_levels)

        # check if the ant is on food
        if self.on_food:
            # pick up food
            if not self.carry_food:
                self.environment.food.grid[self.pos] -= 1
            self.carry_food = True
            self.environment.path_lengths.append(len(self.history)+1)

        # drop pheromones if carrying food
        if self.carry_food:
            self.environment.place_pheromones(self.pos)

        # if on the colony, drop food and remove history
        if self.on_colony:
            self.carry_food = False
            self.history = [self.pos]


    @property
    def on_colony(self):
        """
        Checks whether the ant is on top of its own colony
        :return: True if on colony, False otherwise
        """
        return self.colony.on_colony(self.pos)

    @property
    def on_food(self):
        """
        Checks whether the ant is on top of a food source
        :return: True if on food, False otherwise
        """
        return self.pos in self.environment.food.get_food_pos()

    def move(self, positions, pheromone_levels):
        """
        Move the ant around the grid. If the ant is carrying food it walks back its original path, otherwise it decides
        where to walk too depending on which positions it can go to, and the pheromone levels of those positions
        :param positions: list of x, y tuples [(x, y), ...]
        :param pheromone_levels: list of floats describing the pheromone level on the respective position
        :return: the new position (x, y)
        """
        if self.carry_food:
            self.environment.move_agent(self, self.history.pop())
        else:
            pheromone_levels = np.array(pheromone_levels) + 0.1
            probabilities = pheromone_levels / sum(pheromone_levels)
            move_to = positions[np.random.choice(np.arange(len(positions)), p=probabilities)]

            self.environment.move_agent(self, move_to)
            self.add_pos_to_history()

    def add_pos_to_history(self):
        """
        Add current position to the history, keeps track of duplicate positions and cuts of the resulting loop
        """
        self.history.append(self.pos)

        first_occurrence = self.history.index(self.pos)
        if first_occurrence != len(self.history) - 1:
            self.history = self.history[:first_occurrence + 1]
