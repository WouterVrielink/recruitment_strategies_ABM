import numpy as np
from mesa import Agent
import matplotlib.patches as patches
from obstacle import Obstacle


class Ant(Agent):
    """An agent with fixed legs."""
    def __init__(self, unique_id, colony):
        super().__init__(unique_id, colony.environment)

        # Agent constants
        self.persistance = 2
        self.memory = 3
        self.environment = colony.environment
        self.colony = colony
        self.pheromone_id = colony.pheromone_id

        # Agent attributes
        self.alive = True
        self.slowScore = 0
        self.pos = colony.pos
        self.history = [colony.pos]

        self.carry_food = 0
        self.carry_capacity = abs(np.random.normal(10))

        self.energy = self.max_energy = abs(np.random.normal(15))
        self.energy_consumption = np.abs(np.random.normal(0.07,0.25))

        self.last_steps = [self.pos for _ in range(self.memory)]

        self.path_lengths = [np.inf]

        # Inform environment
        self.environment.grid.place_agent(self, self.pos)

        # Animation attributes
        self._patch = None
        self.size = 0.4

    def step_energy(self):
        """
        Use energy and check if the agent is now dead.
        """
        self.energy -= self.energy_consumption

        if self.energy <= 0:
            self.die()

    def check_food(self):
        # check if the ant is on food
        if self.on_food:
            # pick up food
            if not self.carry_food:
                self.environment.food.grid[self.pos] -= self.carry_capacity
                print(self.environment.food.grid[self.pos])
                self.carry_food = self.carry_capacity

            #TODO dit is raar
            self.consume(colony=False)
            self.environment.path_lengths.append(len(self.history) + 1)


    def step(self):
        """
        Do a single time-step. Function called by colony
        """
        if not self.alive:
            return

        self.encounters = 0

        # Use energy
        self.step_energy()

        # Get the possible positions to move too, and their respective pheromone levels
        positions, pheromone_levels = self.environment.get_neighbor_pheromones(self.pos, self.pheromone_id)

        # Store current position and move to the next
        self.move(positions, pheromone_levels)

        # TODO, waar moet dit heen
        self.encounters += self.count_encounters()

        # Check if the agent is on top of food
        self.check_food()

        # drop pheromones if carrying food
        if self.carry_food > 0:
            self.environment.place_pheromones(self.pos)

        # if on the colony, drop food and remove history
        if self.on_colony:
            self.colony.stash_food(self.carry_food)
            self.carry_food = 0
            self.history = [self.pos]
            self.consume(colony=True)

    @property
    def on_obstacle(self):
        """
        Checks if ant is currently at an obstacle, and returns this obstacle.
        """
        return any([isinstance(x, Obstacle) for x in self.environment.grid[self.pos[0]][self.pos[1]]])

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
        """
        if self.slowScore == 0:
            if self.carry_food:
                self.environment.move_agent(self, self.history.pop())
            else:
                # Calculate pheromone bias
                pheromone_levels = np.array(pheromone_levels) + 0.1
                pheromone_probabilities = pheromone_levels / sum(pheromone_levels)

                # Calculate direction bias
                direction = np.subtract(self.pos, self.last_steps[0])
                direction_probabilities = np.zeros(len(positions))

                # Use the length of the summed vector to see if the angle is smaller than 40-ish degrees
                for i, pos in enumerate(positions):
                    vecsum = direction + pos

                    if vecsum[0] ** 2 + vecsum[1] ** 2 > 2.1:
                        direction_probabilities[i] = np.dot(direction, np.subtract(pos, self.last_steps[0]))

                # Prevent weird bug (ants going to left bottom)
                if direction_probabilities.any() == np.zeros(len(positions)).any():
                    probabilities = pheromone_probabilities
                else:
                    direction_probabilities /= sum(direction_probabilities)

                    # Combine pheromone and direction bias
                    probabilities = [p + self.persistance * d for p, d in zip(pheromone_probabilities, direction_probabilities)]

                # Normalise
                probabilities /= sum(probabilities)

                move_to = positions[np.random.choice(np.arange(len(positions)), p=probabilities)]

                self.environment.move_agent(self, move_to)
                self.add_pos_to_history()

            if self.on_obstacle:
                self.slowScore += [x for x in self.environment.grid[self.pos[0]][self.pos[1]] if isinstance(x, Obstacle)][0].cost
        else:
            self.slowScore -= 1

    def add_pos_to_history(self):
        """
        Add current position to the history, keeps track of duplicate positions and cuts of the resulting loop
        """
        if not self.on_food:
            self.history.append(self.pos)
            first_occurrence = self.history.index(self.pos)
            if first_occurrence != len(self.history) - 1:
                self.history = self.history[:first_occurrence + 1]
            self.last_steps.append(self.pos)
            self.last_steps.pop(0)

    def update_vis(self):
        """
        :return:
        """
        if not self._patch:
            self._patch = patches.Rectangle(self.environment.grid_to_array(self.pos), 0.4, 0.4, linewidth=2,
                                            edgecolor='k', facecolor='w', fill=True, zorder=2)
            self.environment.ax.add_patch(self._patch)
        else:
            if self.carry_food:
                self._patch.set_facecolor('g')
            else:
                self._patch.set_facecolor('w')
            if not self.alive:
                self._patch.set_facecolor('black')
            pos = self.environment.grid_to_array(self.pos)
            pos = (pos[0] + (1 - self.size) / 2, pos[1] + (1 - self.size) / 2)
            self._patch.set_xy(pos)

        return self._patch

    def count_encounters(self):
        counter = 0
        agents = self.environment.grid.get_neighbors(include_center=True, radius = 0, pos=self.pos, moore=self.environment.moore)
        for agent in agents:
            if type(agent) == type(self):
                counter += 1
        return counter

    def die(self):
        self.alive = False

    def consume(self, colony):
        consumption = self.max_energy - self.energy
        if colony:
            self.colony.food_stash -= consumption
        else:
            self.environment.food.grid[self.pos] -= consumption
        self.energy = self.max_energy
