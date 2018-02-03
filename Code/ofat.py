__author__ = 'Wessel Klijnsma'
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from SALib.sample import saltelli
from SALib.analyze import sobol
from roles import Unassigned, Follower, Leader, Pheromone
from batchrunner import BatchRunner
from copy import copy
from model import Environment

default_params = [5.60426548e-01, 4.86656242e-01, 5.23613688e-01, 5.44587569e-01,
                  2.50770030e-01, 2.74353174e-01, 5.17588437e-01, 100,
                  1.14958368e+01]
ranges = [np.linspace(0, 1), np.linspace(0, 1), np.linspace(0, 1),
          np.linspace(0, 1), np.linspace(0, 1), np.linspace(0, 0.5),
          np.linspace(0, 1), range(10, 200, 10), range(3, 20)]
param_names = ['p_uf', 'p_pu', 'p_up', 'p_fl', 'p_lu', 'g', 'ratio', 'N', 'size']
param_values = []

max_steps = 500
replicates = 10
model_reporters = {"unassigned": lambda m: sum([1 if a.role == Unassigned else 0 for a in m.schedule.agents]),
                   "followers": lambda m: sum([1 if a.role == Follower else 0 for a in m.schedule.agents]),
                   "leaders": lambda m: sum([1 if a.role == Leader else 0 for a in m.schedule.agents]),
                   "pheromone": lambda m: sum([1 if a.role == Pheromone else 0 for a in m.schedule.agents])}

for i in range(len(param_names)):
    for v in ranges[i]:
        param_set = copy(default_params)
        param_set[i] = v
        param_values.append(tuple(param_set))

    batch = BatchRunner(Environment, param_sets=param_values, param_names=param_names, max_steps=max_steps,
                        iterations=replicates, model_reporters=model_reporters)
    batch.run_all(4)
    data = batch.get_model_vars_dataframe()
    data.to_csv('../Data/ofat_full2/ofat_3_2_1_' + param_names[i] + '.csv')
    param_values = []
