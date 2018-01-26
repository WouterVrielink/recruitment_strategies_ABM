from model import Environment
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from roles import Unassigned, Follower, Leader, Pheromone
from batchrunner import BatchRunner

def plot_p_fl(df):
    """Creates the p vs (f + l) plot"""

    plt.figure()
    plt.scatter(df['pheromone'], df['followers'] + df['leaders'])
    plt.xlabel(r'$p$')
    plt.ylabel(r'$f + l$')
    plt.show()


def plot_col(df, cols):
    """Plots the variables in the cols array"""

    plt.figure()
    df[cols].plot()
    plt.show()


def plot_continuous(env, steps=1000):
    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.set_xlim([0, env.width])
    ax.set_ylim([0, env.height])
    env.animate(ax)
    fig_num = plt.get_fignums()[0]

    for i in range(steps):
        if not plt.fignum_exists(fig_num): return False

        plt.title('iteration: ' + str(i))
        plt.pause(0.001)

        # take a step
        env.step()

        # store the state for animation
        env.animate(ax)
        fig.canvas.draw()
    return True


if __name__ == '__main__':
    # env = Environment(p_up=0.2)
    # plot_continuous(env, 200)
    # data = env.dc.get_model_vars_dataframe()
    # plot_col(data, ['unassigned', 'followers', 'leaders', 'pheromone'])
    # replicates = 3
    # max_steps = 500
    # model_reporters = {"unassigned": lambda m: sum([1 if a.role == Unassigned else 0 for a in m.schedule.agents]),
    #                    "followers": lambda m: sum([1 if a.role == Follower else 0 for a in m.schedule.agents]),
    #                    "leaders": lambda m: sum([1 if a.role == Leader else 0 for a in m.schedule.agents]),
    #                    "pheromone": lambda m: sum([1 if a.role == Pheromone else 0 for a in m.schedule.agents])}
    # var_params = {"p_pu": np.arange(0, 1, 0.3), "p_uf": np.arange(0, 1, 0.3)}
    # fixed_params = {"N": 100, "g": 10, "w": 50, "h": 50, "p_up": 0.5, "p_fl": 0.01}
    # batch_run = BatchRunner(Environment, variable_parameters=var_params, fixed_parameters=fixed_params,
    #                         max_steps=max_steps, iterations=replicates, model_reporters=model_reporters)
    # batch_run.run_all(1)

    env = Environment(moore=False)

    for _ in range(10000):
        env.step()

    # data = batch_run.get_model_vars_dataframe()
    # plot_p_fl(data)
