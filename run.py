from colony import Colony
from environment import Environment

env = Environment(width=10, height=10, n_colonies=1, n_ants=1)

steps = 1000
for _ in range(steps):
    env.step()

for agent in Environment.ant_list:
    print(agent.location)