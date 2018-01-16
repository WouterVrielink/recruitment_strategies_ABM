from mesa import Agent
import numpy as np

class Obstacle(Agent):
    """An obstacle kind of agent."""

    def __init__(self, environment, pos=None, cost=10):
        self.environment = environment
        self.cost = cost

        # make sure that obstacle can't be at same place as food or colony
        # TODO: obstacle should not be placed on colony or obstacle itself
        if pos == None:
            pos = self.environment.get_random_location()

            while(self.environment.position_taken(pos)):
                pos = self.environment.get_random_location()

        self.pos = pos

        # register self
        self.environment.grid.place_agent(self, self.pos)

    def on_obstacle(self, pos):
        return pos == self.pos
