from model import Environment
import matplotlib.pyplot as plt
import numpy as np
from mesa.batchrunner import BatchRunner


def plot_p_fl(df):
    """Creates the p vs (f + l) plot"""

    plt.figure()
    plt.plot(df['pheromone'], df['followers'] + df['leaders'])
    plt.show()


def plot_col(df, cols):
    """Plots the variables in the cols array"""

    plt.figure()
    df[cols].plot()
    plt.show()


if __name__ == '__main__':
    replications = 5
    max_steps = 1000
    model_reporters = {"unassigned": lambda m: sum([1 if a.role == 0 else 0 for a in m.schedule.agents]),
                       "followers": lambda m: sum([1 if a.role == 1 else 0 for a in m.schedule.agents]),
                       "leaders": lambda m: sum([1 if a.role == 2 else 0 for a in m.schedule.agents]),
                       "pheromone": lambda m: sum([1 if a.role == 3 else 0 for a in m.schedule.agents])}

    var_params = {"N": np.arange(10, 100, 10)}
    fixed_params = {"g": 10, "w": 50, "h": 50, "p_uf": 0.5, "p_ul": 0.5, "p_up": 0.5, "p_fl": 0.5}
    batch_run = BatchRunner(Environment, variable_parameters=var_params, fixed_parameters=fixed_params,
                            max_steps=max_steps, iterations=replications, model_reporters=model_reporters)
    batch_run.run_all(4)
    data = batch_run.get_model_vars_dataframe()
