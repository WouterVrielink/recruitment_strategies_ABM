import matplotlib.pyplot as plt

import pandas as pd
import numpy as np
from SALib.analyze import sobol

def plot_index(s, params, i):
    indices = s['S' + i]
    errors = s['S' + i + '_conf']
    l = len(indices)
    plt.figure()
    plt.ylim([-0.2, len(indices)-1+0.2])
    plt.yticks(range(l), params)
    plt.errorbar(indices, range(l), xerr=errors, linestyle='None', marker='o')
    plt.axvline(0, c='k')

data = pd.read_csv('../Data/batchrun01-02-2018.csv')

data['total'] = np.round(data['N'] // 2) + np.round((data['N'] // 2) * data['ratio']) + data['N'] - np.round(data['N'] // 2) - np.round(
    (data['N'] // 2) * data['ratio'])

data['pfl_net'] = (data['pheromone'] - data['followers'] - data['leaders']) / data['total']
data['pu_net'] = (data['pheromone'] - data['unassigned']) / data['total']
data['flu_net'] = (data['followers'] + data['leaders'] - data['unassigned']) / data['total']


X = data[['p_uf', 'p_pu', 'p_up', 'p_fl', 'p_lu', 'g', 'ratio', 'N', 'size']].as_matrix()

problem = {
    'num_vars': 9,
    'names': ['p_uf', 'p_pu', 'p_up', 'p_fl', 'p_lu', 'g', 'ratio', 'N', 'size'],
    'bounds': [[0, 1]] * 5 + [[0, 0.5]] + [[0, 1]] + [[10, 200]] + [[3, 20]]
}
Si = sobol.analyze(problem, data['pu_net'].as_matrix(), print_to_console=True)
print(Si)
plot_index(Si, ['p_uf', 'p_pu', 'p_up', 'p_fl', 'p_lu', 'g', 'ratio', 'N', 'size'], '1')
plt.show()
