import matplotlib.pyplot as plt
from sklearn.discriminant_analysis import QuadraticDiscriminantAnalysis
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis
from scipy import stats
from mpl_toolkits.mplot3d import Axes3D

import pandas as pd
import numpy as np
from SALib.analyze import sobol

data = pd.read_csv('29-01-2018_5000.csv')
cls = (data['unassigned'] == 55) + ((data['pheromone'] == 0) & ((data['leaders'] + data['followers']) != 0)) * 2 + \
      (((data['leaders'] == 0) & (data['followers'] == 0)) & (data['pheromone'] != 0)) * 3 + \
      ((data['leaders'] == 0) & (data['followers'] != 0)) * 4
data['class'] = cls
data['p1'] = data['class'] == 1
data['p2'] = data['class'] == 2
data['p3'] = data['class'] == 3
data['p5'] = data['class'] == 0
data['g'] = np.floor(data['g'])
data['percentage'] = (data['followers'] + data['leaders']) / 55
data['pfl_ratio'] = (data['followers'] + data['leaders']) / (data['pheromone'] + 1)
data['pfl_net'] = (data['pheromone'] - data['followers'] - data['leaders']) / 55
data['pu_net'] = (data['pheromone'] - data['unassigned']) / 55
data['flu_net'] = (data['followers'] + data['leaders'] - data['unassigned']) / 55



# fig = plt.figure()
# ax = fig.add_subplot(311)
# ax.scatter(data['pfl_net'], data['pu_net'])
# plt.xlabel('p - fl')
# plt.ylabel('p - u')
#
# ax.subfigure()
# ax.scatter(data['pfl_net'], data['flu_net'])
# plt.xlabel('p - fl')
# plt.ylabel('fl - u')
#
# ax.subfigure()
# ax.scatter(data['flu_net'], data['pu_net'])
# plt.xlabel('fl - u')
# plt.ylabel('p - u')

# plt.figure()
# plt.scatter(data['p_lu'], data['flu_net'])
plt.show()
#
#SA
X = data[['p_uf', 'p_pu', 'p_up', 'p_fl', 'p_lu', 'g']].as_matrix()



problem = {
    'num_vars': 6,
    'names': ['p_uf', 'p_pu', 'p_up', 'p_fl', 'p_lu', 'g'],
    'bounds': [[0, 1]] * 5 + [[0, 5]]
}
Si = sobol.analyze(problem, data['pfl_net'].as_matrix(), print_to_console=True)

#
#
# params = ['p_uf', 'p_pu', 'p_up', 'p_fl', 'p_lu']
# # for param in params:
# Si = sobol.analyze(problem, y, print_to_console=True)
# # print(data['class'])
# # all_labels = [('p1', 1), ('p2', 2), ('p3', 3), ('p5', 0)]
