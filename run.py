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
	for colony in env.colonies:
		for agent in colony.ant_list.agents:
			counter += agent.encounters
	return counter/2



def plot_continuous(env, steps = 1000):
    fig = plt.figure()
    ax = fig.add_subplot(111)
    env.animate(ax)

    pheromones = []

    ant_positions = [[] for _ in range(steps + 1)]
    colony_positions = [[] for _ in range(steps + 1)]
    food_positions = [[] for _ in range(steps + 1)]
    ant_foods = [[] for _ in range(steps + 1)]

    store_state(0, pheromones, colony_positions, food_positions, ant_positions, ant_foods)

    fig, ax, im, colony_patches, food_patches, ant_patches = init_figure(pheromones, colony_positions, food_positions, ant_positions, ant_foods)

    im = ax.imshow(np.zeros((width, height)), vmin=0, vmax=100,
                       interpolation='None',
                       cmap="Purples")


    plt.ion()
    fig.show()
    for i in range(steps):
        plt.title('iteration: ' + str(i))
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

    env = Environment(width=width, height=height, n_colonies=1, n_ants=100, n_obstacles=10, decay=0.99, sigma=0.2, moore=True)

    # compute_then_plot(env, steps)
    plot_continuous(env, steps=steps)
