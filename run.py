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
    fig_num = plt.get_fignums()[0]
    for i in range(steps):
        if not plt.fignum_exists(fig_num): return False
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
    return True


def compute_no_plot(env, steps):
    for _ in range(steps):
        env.step()


def plot_col(df, col):
    plt.figure()
    plt.ylim([0, np.max(df[col])])
    plt.xlabel('iteration')
    plt.ylabel(col)
    df[col].plot()


def animate_distribution(path_lengths, steps):
    fig = plt.figure()
    ax = fig.add_subplot(111)
    for i in range(steps):
        ax.clear()
        t_data = path_lengths.loc[i]
        t_data = t_data[t_data != np.inf]
        t_data.hist(ax=ax)
        plt.pause(0.001)


if __name__ == '__main__':
    width = 20
    height = 20
    steps = 1000
    ant_size = 0.4

    env = Environment(width=width, height=height, n_colonies=1, n_ants=100, n_obstacles=0, decay=0.99, sigma=0.2,
                      moore=False)
    plot_continuous(env, steps)
    # compute_then_plot(env, steps)
    # compute_no_plot(env, steps=steps)
    model_data = env.datacollector.get_model_vars_dataframe()
    agent_min_paths = env.datacollector.get_agent_vars_dataframe()
    plot_col(model_data, 'Mean minimum path length')
    plt.show()
