from mesa import Agent
import numpy as np
import matplotlib.patches as patches


class Obstacle(Agent):
    """An obstacle kind of agent."""
    def __init__(self, environment, pos=None, cost=10):
        self.environment = environment
        self.cost = cost
        self.width = environment.width
        self.height = environment.height
        self.grid = np.zeros((self.width, self.height))
        self._patch = None

        # make sure that obstacle can't be at same place as food or colony
        # TODO: obstacle should not be placed on colony or obstacle itself
        if pos == None:
            x = np.random.randint(0, self.width - 1, 1)
            y = np.random.randint(0, self.height - 1, 1)
            while (True):
                for j, k in np.array(np.where(environment.food.grid > 0)).T:
                    if (j, k) == (x ,y): # get new location
                        x = np.random.randint(0, self.width - 1, 1)
                        y = np.random.randint(0, self.height - 1, 1)
                    else:
                        self.pos = (x[0],y[0])
                        break
                break
        else:
            self.pos = pos

        # register self
        self.environment.grid.place_agent(self, self.pos)

    def getRandomLocation(self):
        return(np.random.randint(0, self.width - 1, 1), np.random.randint(0, self.height - 1, 1))

    def checkLegalLocation(self, pos):
        for x, y in np.array(np.where(env.food.grid > 0)).T:
            if (x,y) == pos:
                return False
            else:
                return True

    def getLegalLocation(self):
        while(True):
            pos = getRandomLocation()
            if checkLegalLocation(pos) == True:
                return pos

    def update_vis(self):
        radius = 0.35
        if not self._patch:
            self._patch = patches.Circle(self.environment.grid_to_array(self.pos), radius, linewidth=2,
                                            edgecolor='k', facecolor='k', fill=True)
            self.environment.ax.add_patch(self._patch)
        else:
            pos = self.environment.grid_to_array((self.pos[0] + 0.5, self.pos[1] - 0.5))
            self._patch.center = pos

        return self._patch

