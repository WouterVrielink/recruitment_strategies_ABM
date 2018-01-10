from colony import AntColony
from environment import Environment

colony1 = AntColony(100)

steps = 1000

for _ in range(steps):
    colony1.step()
