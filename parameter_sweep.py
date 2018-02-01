from SALib.sample import saltelli
from SALib.analyze import sobol
from SALib.test_functions import Ishigami
import numpy as np
from model import Environment
import matplotlib.pyplot as plt
import pandas as pd
from roles import Unassigned, Follower, Leader, Pheromone
from batchrunner import BatchRunner

if __name__ == '__main__':
    problem = {
        'num_vars': 5,
        'names': ['p_uf', 'p_pu', 'p_up', 'p_fl', 'p_lu'],
        'bounds': [[0, 1]] * 5
    }

    param_values = saltelli.sample(problem, 10)
    print(len(param_values))
    param_sets = [tuple(param_values[i, :]) for i in range(len(param_values))]
    param_names = ['p_uf', 'p_pu', 'p_up', 'p_fl', 'p_lu']
    max_steps = 500
    replicates = 1

    model_reporters = {"unassigned": lambda m: sum([1 if a.role == Unassigned else 0 for a in m.schedule.agents]),
                       "followers": lambda m: sum([1 if a.role == Follower else 0 for a in m.schedule.agents]),
                       "leaders": lambda m: sum([1 if a.role == Leader else 0 for a in m.schedule.agents]),
                       "pheromone": lambda m: sum([1 if a.role == Pheromone else 0 for a in m.schedule.agents])}
    batch = BatchRunner(Environment, param_sets=param_sets, param_names=param_names, max_steps=max_steps,
                        iterations=replicates, model_reporters=model_reporters)
    batch.run_all(4)
    data = batch.get_model_vars_dataframe()
    Si = sobol.analyze(problem, data['leaders'].as_matrix(), print_to_console=True)

