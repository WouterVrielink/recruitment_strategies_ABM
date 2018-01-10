from colony import Colony
from environment import Environment

colony1 = Colony(100)

steps = 1000

for _ in range(steps):
    colony1.step()
