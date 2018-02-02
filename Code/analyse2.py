import matplotlib.pyplot as plt
from sklearn.discriminant_analysis import QuadraticDiscriminantAnalysis
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis
from scipy import stats
from mpl_toolkits.mplot3d import Axes3D

import pandas as pd
import numpy as np
from SALib.analyze import sobol

data = pd.read_csv('../Data/batchrun01-02-2018.csv')

data['total'] = np.round(data['N'] // 2) + np.round((data['N'] // 2) * data['ratio']) + data['N'] - np.round(data['N'] // 2) - np.round(
    (data['N'] // 2) * data['ratio'])

cls = (data['unassigned'] == data['total']) + ((data['pheromone'] == 0) & ((data['leaders'] + data['followers']) != 0)) * 2 + \
      (((data['leaders'] == 0) & (data['followers'] == 0)) & (data['pheromone'] != 0)) * 3 + \
      ((data['leaders'] == 0) & (data['followers'] != 0)) * 4
data['class'] = cls
data['p1'] = data['class'] == 1
data['p2'] = data['class'] == 2
data['p3'] = data['class'] == 3
data['p5'] = data['class'] == 0
data['g'] = np.floor(data['g'])
data['percentage'] = (data['followers'] + data['leaders']) / data['total']
data['pfl_ratio'] = (data['followers'] + data['leaders']) / (data['pheromone'] + 1)
data['pfl_net'] = (data['pheromone'] - data['followers'] - data['leaders']) / data['total']
data['pu_net'] = (data['pheromone'] - data['unassigned']) / data['total']
data['flu_net'] = (data['followers'] + data['leaders'] - data['unassigned']) / data['total']

# fig = plt.figure()
# plt.scatter(data['pfl_net'], data['pu_net'])
# plt.xlabel('p - fl')
# plt.ylabel('p - u')
#
# fig = plt.figure()
# plt.scatter(data['pfl_net'], data['flu_net'])
# plt.xlabel('p - fl')
# plt.ylabel('fl - u')
#
# fig = plt.figure()
# plt.scatter(data['flu_net'], data['pu_net'])
# plt.xlabel('fl - u')
# plt.ylabel('p - u')
#
# plt.figure()
# plt.scatter(data['p_lu'], data['flu_net'])
# plt.show()
#
# SA
X = data[['p_uf', 'p_pu', 'p_up', 'p_fl', 'p_lu', 'g', 'ratio', 'N', 'size']].as_matrix()

problem = {
    'num_vars': 9,
    'names': ['p_uf', 'p_pu', 'p_up', 'p_fl', 'p_lu', 'g', 'ratio', 'N', 'size'],
    'bounds': [[0, 1]] * 5 + [[0, 0.5]] + [[0, 1]] + [[10, 200]] + [[3, 20]]
}
Si = sobol.analyze(problem, data['pu_net'].as_matrix(), print_to_console=True)

#
#
# params = ['p_uf', 'p_pu', 'p_up', 'p_fl', 'p_lu']
# # for param in params:
# Si = sobol.analyze(problem, y, print_to_console=True)
# # print(data['class'])
# # all_labels = [('p1', 1), ('p2', 2), ('p3', 3), ('p5', 0)]
