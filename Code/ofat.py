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

# [[ 0.5782103   0.00238012  0.84082242  0.59827735 -0.06291654  2.01866334]
#  [ 0.521836    0.02786532  0.81961924  0.53805511  0.30298033  2.00602107]
#  [ 0.53758599  0.48311026  0.51411553  0.54012785  0.25608399  2.00812818]
#  [ 0.59396029  0.45762505  0.5353187   0.60035009 -0.10981289  2.02077046]]

default_params = [0.55789815, 0.24274519, 0.67746897, 0.5692026, 0.09658372, 2, 20, 20]
ranges = [np.linspace(0.4, 0.7, 40), np.linspace(0, 0.7, 40), np.linspace(0.3, 0.9, 40),
          np.linspace(0.3, 0.8, 40), np.linspace(0, 0.5, 40), np.floor(np.linspace(1, 20, 40)),
          range(2, 42), range(2, 42)]
param_names = ['p_uf', 'p_pu', 'p_up', 'p_fl', 'p_lu', 'g', 'w', 'h']
param_values = []

for i in range(len(param_names)):
    for v in ranges[i]:
        param_set = copy(default_params)
        param_set[i] = v
        param_values.append(tuple(param_set))

max_steps = 5
replicates = 1
model_reporters = {"unassigned": lambda m: sum([1 if a.role == Unassigned else 0 for a in m.schedule.agents]),
                   "followers": lambda m: sum([1 if a.role == Follower else 0 for a in m.schedule.agents]),
                   "leaders": lambda m: sum([1 if a.role == Leader else 0 for a in m.schedule.agents]),
                   "pheromone": lambda m: sum([1 if a.role == Pheromone else 0 for a in m.schedule.agents])}
batch = BatchRunner(Environment, param_sets=param_values, param_names=param_names, max_steps=max_steps,
                    iterations=replicates, model_reporters=model_reporters)
batch.run_all(4)
data = batch.get_model_vars_dataframe()
data.to_csv('ofat_1_2_3.csv')
