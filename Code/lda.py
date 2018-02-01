from sklearn.discriminant_analysis import LinearDiscriminantAnalysis
from matplotlib.patches import Polygon

import matplotlib.pyplot as plt
import pandas as pd
import numpy as np


params = ['p_uf', 'p_pu', 'p_up', 'p_fl', 'p_lu', 'g']
file_path = '../Data/batchrun01-02-2018.csv'

data = pd.read_csv(file_path)

# this should not be necessary
cls = (data['unassigned'] == 55) + ((data['pheromone'] == 0) & ((data['leaders'] + data['followers']) != 0)) * 2 + \
      (((data['leaders'] == 0) & (data['followers'] == 0)) & (data['pheromone'] != 0)) * 3 + \
      ((data['leaders'] == 0) & (data['followers'] != 0)) * 4
data['class'] = cls
data['g'] = np.floor(data['g'])

# extract relevant columns
X = data[params].as_matrix()
y = data['class'].as_matrix()

# do a lda over it
lda = LinearDiscriminantAnalysis(n_components=2, solver='svd')
lda.fit(X, y)

# project the data on the new axes
X_2 = lda.fit_transform(X, y)

# check the explained variance of the data projection
print("The two new axes of the projection explain respectively {} of the variance, and are combined {} of the variance."
      .format(lda.explained_variance_ratio_, np.sum(lda.explained_variance_ratio_)))

# check the relative contribution of each parameter to the axes
abs_scalings = np.abs(lda.scalings_[:,:2])
rel_scalings = (abs_scalings / np.sum(abs_scalings, axis=0)).T
rel_scalings = pd.DataFrame(rel_scalings, index=['x', 'y'], columns=params)
print("The relative scaling of each parameter to the axes is given in this table:\n{}\n"
      .format(rel_scalings))

# make a scatter plot of the projection and the classes
ax = plt.gca()
for group in [0, 1, 2, 3]:
    plt.scatter(X_2[y == group, 0], X_2[y == group, 1], alpha=.8, label=group, s=0.5)

# select which part of the data we want to sample more intensely
corners = np.array([[-3, -2.5],
                    [-3, -1],
                    [0, -1],
                    [0, -2.5]])

def inv_transform(lda, x):
    inv = np.linalg.pinv(lda.scalings_[:,:2])
    return np.dot(x, inv) + lda.xbar_

# transform these 2D points back to their original dimension
all = inv_transform(lda, corners)

# get some basic descriptives out of these variables
mins = np.min(all, axis=0)
maxs = np.max(all, axis=0)
avgs = np.mean(all, axis=0)
minmax = pd.DataFrame(np.stack((mins, maxs)), index=['min', 'max'], columns=params)
print("The min and max values of each param in the selected area are:\n{}\n"
      .format(minmax))

# lets check how well a meshgrid between the min and max of each parameter fits in between the selected area
acc = 10
param_ranges = []
for i, param in enumerate(params):
    param_ranges.append(np.linspace(mins[i],maxs[i],acc))
mesh = np.meshgrid(*param_ranges)
positions = lda.transform(np.vstack(map(np.ravel, mesh)).T)
corners = [np.argmin(positions[:, 0]),
           np.argmin(positions[:, 1]),
           np.argmax(positions[:, 0]),
           np.argmax(positions[:, 1])]
corners = positions[corners]
polygon = Polygon(corners, True, alpha=1, edgecolor='k', linewidth=2, fill=False)
ax.add_patch(polygon)

# make the final plot
plt.legend()
plt.show()