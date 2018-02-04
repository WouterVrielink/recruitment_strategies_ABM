# -*- coding: utf-8 -*-
"""
Does a parameter sweep over the data. Set each of the bounds in the 'problem'
dictionary.
"""
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

from SALib.sample import saltelli

from batchrunner import BatchRunner
from model import Environment
from roles import Unassigned, Follower, Leader, Pheromone

if __name__ == '__main__':
    # Set the variables and their respective bounds
    problem = {
        'num_vars': 9,
        'names': ['p_uf', 'p_pu', 'p_up', 'p_fl', 'p_lu', 'g', 'ratio', 'N', 'size'],
        'bounds': [[0, 1]] * 5 + [[0, 0.5]] + [[0, 1]] + [[10, 500]] + [[3, 20]]
    }
    problem = {
        'num_vars': 7,
        'names': ['p_uf', 'p_pu', 'p_up', 'p_fl', 'p_lu', 'g', 'ratio'],
        'bounds': [[0.55, 0.68], [0, 0.62], [0.41, 0.97], [0.54, 0.64], [0, 0.3], [0.27, 0.32], [0.45, 0.5]]
    }

<<<<<<< Updated upstream
    # Prepare a sample
    param_values = saltelli.sample(problem, 10)
    param_values[:,7] = np.round(param_values[:,7])
    param_values[:,8] = np.round(param_values[:,8])
=======
    # param_values[:,7] = np.round(param_values[:,7])
    # param_values[:,8] = np.round(param_values[:,8])
    param_values = saltelli.sample(problem, 2500)
>>>>>>> Stashed changes

    # Create sets of parameters
    param_sets = [tuple(param_values[i, :]) for i in range(len(param_values))]

    param_names = problem['names']

    # Set the repetitions and the amount of steps
    replicates = 1
    max_steps = 500

    fixed_params = {'N': 40, 'size': 11}

    model_reporters = {"unassigned": lambda m: sum([1 if a.role == Unassigned else 0 for a in m.schedule.agents]),
                       "followers": lambda m: sum([1 if a.role == Follower else 0 for a in m.schedule.agents]),
                       "leaders": lambda m: sum([1 if a.role == Leader else 0 for a in m.schedule.agents]),
                       "pheromone": lambda m: sum([1 if a.role == Pheromone else 0 for a in m.schedule.agents])}

    batch = BatchRunner(Environment, param_sets=param_sets, param_names=param_names, max_steps=max_steps,
<<<<<<< Updated upstream
                        iterations=replicates, model_reporters=model_reporters)

    # Run the batchrunner on 7 cores.
=======
                        iterations=replicates, model_reporters=model_reporters, fixed_parameters=fixed_params)
>>>>>>> Stashed changes
    batch.run_all(7)

    # Get the data and write it to disk
    data = batch.get_model_vars_dataframe()
<<<<<<< Updated upstream
    data.to_csv("../Data/batchrun01-02-2018.csv", index=False)
=======
    for param, value in fixed_params.items():
        data[param] = value
    data.to_csv("../Data/batchrun03-02-2018_square.csv", index=False)

    Si = sobol.analyze(problem, data['leaders'].as_matrix(), print_to_console=True)

>>>>>>> Stashed changes
