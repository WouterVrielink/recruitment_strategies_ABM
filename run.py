from model import Environment
import matplotlib.pyplot as plt
import numpy as np
from matplotlib import animation
import matplotlib.patches as patches
import itertools


def compute_then_plot(env, steps):
    raise NotImplementedError


def total_encounters(env):
    counter = 0

    for agent in env.schedule.agents:
        counter += agent.encounters
    return counter / 2


def plot_continuous(env, steps=1000):
    fig = plt.figure()
    ax = fig.add_subplot(111)
    env.animate(ax)
    for i in range(steps):
        ants_alive = 0
        for ant in env.schedule.agents:
            if ant.alive:
                ants_alive += 1
        plt.title('iteration: ' + str(i) + " || No. ants: " + str(ants_alive) + "\nFood stash: " + str(env.colonies[0].food_stash))
        plt.pause(0.001)

        # take a step
        env.step()
        number_of_encounters = total_encounters(env)
        # store the state for animation
        env.animate(ax)
        fig.canvas.draw()


if __name__ == '__main__':
    width = 20
    height = 20
    steps = 2000
    ant_size = 0.4

    env = Environment(width=width, height=height, n_colonies=1, n_ants=100, n_obstacles=10, decay=0.99, sigma=0.2,
                      moore=False)

    # compute_then_plot(env, steps)
    plot_continuous(env, steps=steps)
    min_paths = env.datacollector.get_model_vars_dataframe()
    agent_min_paths = env.datacollector.get_agent_vars_dataframe()
    min_paths.plot()
    plt.show()
