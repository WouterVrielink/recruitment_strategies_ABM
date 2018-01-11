from mesa.time import RandomActivation
from ant import Ant
from mesa import Agent


class Colony(Agent):
    """A model with some number of agents."""
    def __init__(self, environment, pheromone_id, location, N):
        self.environment = environment
        self.pheromone_id = pheromone_id
        self.location = location
        self.num_agents = N
        self.ant_list = RandomActivation(environment)

        # Create agents
        self.add_ants(N)

        # register self
        self.environment.grid.place_agent(self, self.location)


    def step(self):
        '''Advance the model by one step.'''
        self.ant_list.step()

    def add_ants(self, N):
        for i in range(N):
            a = Ant(i, self)
            self.ant_list.add(a)

    
