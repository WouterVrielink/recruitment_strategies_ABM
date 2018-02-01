import matplotlib.pyplot as plt
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis

import pandas as pd
import numpy as np

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
data['ratio'] = (data['pheromone'] + data['leaders'] + data['followers']) / (data['pheromone'] + data['leaders'] + data['followers'] + data['unassigned'])
X = data[['p_uf', 'p_pu', 'p_up', 'p_fl', 'p_lu', 'g']].as_matrix()
y = data['class'].as_matrix()

lda = LinearDiscriminantAnalysis(n_components=2, solver='svd')
lda.fit(X, y)
X_2 = lda.fit_transform(X, y)

for group in [0, 1, 2, 3]:
    plt.scatter(X_2[y == group, 0], X_2[y == group, 1], alpha=.8, label=group, s=0.5)

params_start = np.array([[0.5, 0.5, 0.5, 0.5, 0.5, 3]])
group_cols = ['g', 'r', 'b', 'k', 'y']
def inv_transform(lda, x):
    inv = np.linalg.pinv(lda.scalings_[:,:2])
    return np.dot(x, inv) + lda.xbar_

a = inv_transform(lda, np.array([[-3, -2.5]]))
b = inv_transform(lda, np.array([[-3, -1]]))
c = inv_transform(lda, np.array([[-0, -1]]))
d = inv_transform(lda, np.array([[-0, -2.5]]))

for point in [a, b, c, d]:
    point = lda.transform(point)
    plt.scatter(point[0,0], point[0,1], c='k', s=50)

all = np.vstack((a, b, c, d))
mins = np.min(all, axis=0)
maxs = np.max(all, axis=0)
avgs = np.mean(all, axis=0)

print(avgs)
# acc = 1
# p_uf = np.linspace(mins[0],maxs[0],acc)
# p_pu = np.linspace(mins[1],maxs[1],60)
# # p_pu = np.linspace(0.2,0.21,acc)
# p_up = np.linspace(mins[2],maxs[2],60)
# # p_up = np.linspace(0.65,0.66,acc)
# p_fl = np.linspace(mins[3],maxs[3],acc)
# p_lu = np.linspace(mins[4],maxs[4],60)
# # p_lu = np.linspace(0,0.01,acc)
# g    = np.linspace(mins[5],maxs[5],acc)
# p_pu = np.random.random(100)
# p_up = np.random.random(100)
# p_lu = np.random.random(100)
# mesh = np.meshgrid(p_uf, p_pu, p_up, p_fl, p_lu, g)
# positions = np.vstack(map(np.ravel, mesh)).T
#
# positions_2 = lda.transform(positions)
# plt.scatter(positions_2[:, 0], positions_2[:, 1], alpha=.8, s=0.5, c='b')

abs_scaling = np.abs(lda.scalings_[:,:2])
print(abs_scaling/ np.sum(abs_scaling, axis=0))

plt.legend()
plt.show()