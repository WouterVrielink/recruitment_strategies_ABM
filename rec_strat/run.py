from model import Environment
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
# from mesa.batchrunner import BatchRunner
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
    # env = Environment()
    # plot_continuous(env)

    replications = 1
    max_steps = 1000
    model_reporters = {"unassigned": lambda m: sum([1 if a.role == 0 else 0 for a in m.schedule.agents]),
                       "followers": lambda m: sum([1 if a.role == 1 else 0 for a in m.schedule.agents]),
                       "leaders": lambda m: sum([1 if a.role == 2 else 0 for a in m.schedule.agents]),
                       "pheromone": lambda m: sum([1 if a.role == 3 else 0 for a in m.schedule.agents])}

    var_params = {"N": np.arange(10, 100, 1)}
    fixed_params = {"g": 10, "w": 2, "h": 2, "p_uf": 0.5, "p_ul": 0.5, "p_up": 0.5, "p_fl": 0.5}
    batch_run = BatchRunner(Environment, variable_parameters=var_params, fixed_parameters=fixed_params,
                            max_steps=max_steps, iterations=replications, model_reporters=model_reporters)
    batch_run.run_all(1)
    data = batch_run.get_model_vars_dataframe()
    plot_p_fl(data)
