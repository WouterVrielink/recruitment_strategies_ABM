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

        if [*self.pos] in np.array(np.where(self.environment.food.grid > 0)).T.tolist():
            if not self.carry_food:
                self.environment.food.grid[self.pos] -= 1
            self.carry_food = True
            self.environment.path_lengths.append(len(self.history))
        if [*self.pos] == [*self.colony.pos]:
            self.carry_food = False
            self.history = []

        if self.carry_food:
            self.environment.place_pheromones(self.pos)

        if not self.carry_food:
            self.history.append(self.pos)

    @property
    def on_food(self):
        """
        checks whether the ant is on top of a food source
        :return: True if on food, False otherwise
        """
        return [*self.pos] in np.array(np.where(self.environment.food.grid > 0)).T.tolist()

    def move(self, positions, pheromone_levels):
        if self.carry_food:
            move_to = self.history.pop()
        else:
            pheromone_levels = np.array(pheromone_levels) + 0.1
            probabilities = pheromone_levels / sum(pheromone_levels)
            move_to = positions[np.random.choice(np.arange(len(positions)), p=probabilities)]

        self.environment.move_agent(self, move_to)

        return move_to
