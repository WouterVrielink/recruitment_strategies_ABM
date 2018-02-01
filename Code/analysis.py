__author__ = 'Wessel Klijnsma'
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from SALib.sample import saltelli
from SALib.analyze import sobol

def plot_class_param(df):
    """Creates the p vs (f + l) plot"""

    plt.figure()
    plt.scatter(df['pheromone'], df['followers'] + df['leaders'])
    plt.xlabel(r'$p$')
    plt.ylabel(r'$f + l$')
    plt.show()

if __name__ == '__main__':
    data = pd.read_csv('batchrun1000_25-01-2018.csv', sep=';')
    cls = (data['unassigned'] == 110) + ((data['pheromone'] == 0) & ((data['leaders'] + data['followers']) != 0)) * 2 + \
          (((data['leaders'] == 0) & (data['followers'] == 0)) & (data['pheromone'] != 0)) * 3 + \
          ((data['leaders'] == 0) & (data['followers'] != 0)) * 4
    data['class'] = cls
    data['p1'] = data['class'] == 1
    data['p2'] = data['class'] == 2
    data['p3'] = data['class'] == 3
    data['p5'] = data['class'] == 0

    problem = {
        'num_vars': 5,
        'names': ['p_uf', 'p_pu', 'p_up', 'p_fl', 'p_lu'],
        'bounds': [[0, 1]] * 5
    }

    sobol.analyze(problem, data['p1'].as_matrix(), print_to_console=True)
    print("\n")
    sobol.analyze(problem, data['p2'].as_matrix(), print_to_console=True)
    print("\n")
    Si = sobol.analyze(problem, data['p3'].as_matrix(), print_to_console=True)

