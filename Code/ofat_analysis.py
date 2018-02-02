__author__ = 'Wessel Klijnsma'
import matplotlib.pyplot as plt
from sklearn.discriminant_analysis import QuadraticDiscriminantAnalysis
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis
from scipy import stats
from mpl_toolkits.mplot3d import Axes3D
import pandas as pd
import numpy as np


def plot_param_var(ax, df, param, var):
    x = df.groupby(param).mean().reset_index()[param]
    y = df.groupby(param).mean()[var]
    err = (1.96 * df.groupby(param)[var].std()) / np.sqrt(df.groupby(param).count()[var])
    ax.errorbar(x, y, yerr=err.as_matrix())
    ax.scatter(df[param], df[var])
    ax.set_xlabel(param)
    ax.set_ylabel(var)


def plot_all_vars(df, param):
    params = ['p_uf', 'p_pu', 'p_up', 'p_fl', 'p_lu', 'g', 'w', 'h']
    chunk = 10 * 40
    index = params.index(param)
    df = df.loc[chunk * index:(index + 1) * chunk - 1]

    f, axs = plt.subplots(3, figsize=(7, 10))
    plot_param_var(axs[0], df, param, 'pfl_net')
    plot_param_var(axs[1], df, param, 'pu_net')
    plot_param_var(axs[2], df, param, 'flu_net')


if __name__ == '__main__':
    data = pd.read_csv('ofat_1_2_bigger.csv')
    total = 55
    cls = (data['unassigned'] == total) + ((data['pheromone'] == 0) & ((data['leaders'] + data['followers']) != 0)) * 2 + \
          (((data['leaders'] == 0) & (data['followers'] == 0)) & (data['pheromone'] != 0)) * 3 + \
          ((data['leaders'] == 0) & (data['followers'] != 0)) * 4
    data['class'] = cls
    data['p1'] = data['class'] == 1
    data['p2'] = data['class'] == 2
    data['p3'] = data['class'] == 3
    data['p5'] = data['class'] == 0
    data['g'] = np.floor(data['g'])
    data['percentage'] = (data['followers'] + data['leaders']) / total
    data['pfl_ratio'] = (data['followers'] + data['leaders']) / (data['pheromone'] + 1)
    data['pfl_net'] = (data['pheromone'] - data['followers'] - data['leaders']) / total
    data['pu_net'] = (data['pheromone'] - data['unassigned']) / total
    data['flu_net'] = (data['followers'] + data['leaders'] - data['unassigned']) / total

    params = ['p_uf', 'p_pu', 'p_up', 'p_fl', 'p_lu', 'g', 'w', 'h']
    for param in params:
        print(param)
        plot_all_vars(data, param)
        plt.savefig('results_ofat2/' + param + '.png')
