from mesa import Agent
import numpy as np


class Obstacle(Agent):
    """An obstacle kind of agent."""
    def __init__(self, environment, location=None, cost=10):
        self.environment = environment
        self.cost = cost
        self.width = environment.width
        self.height = environment.height
        self.grid = np.zeros((self.width, self.height))
        # make sure that obstacle can't be at same place as food or colony
        # TODO: obstacle should not be placed on colony or obstacle itself
        if location == None:
            x = np.random.randint(0, self.width - 1, 1)
            y = np.random.randint(0, self.height - 1, 1)
            while (True):
                for j, k in np.array(np.where(environment.food.grid > 0)).T:
                    if (j, k) == (x ,y): # get new location
                        x = np.random.randint(0, self.width - 1, 1)
                        y = np.random.randint(0, self.height - 1, 1)
                    else:
                        self.location = (x[0],y[0])
                        break
                break
        else:
            self.location = location

        # register self
        self.environment.grid.place_agent(self, self.location)

    def getRandomLocation(self):
        return(np.random.randint(0, self.width - 1, 1), np.random.randint(0, self.height - 1, 1))

    def checkLegalLocation(self, location):
        for x, y in np.array(np.where(env.food.grid > 0)).T:
            if (x,y) == location:
                return False
            else:
                return True

    def getLegalLocation(self):
        while(True):
            location = getRandomLocation()
            if checkLegalLocation(location) == True:
                return location
