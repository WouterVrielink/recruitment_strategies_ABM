__author__ = 'Wessel Klijnsma'
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np


def plot_param_var(ax, df, param, var):
    x = df.groupby(param).mean().reset_index()[param]
    y = df.groupby(param).mean()[var]
    replicates = df.groupby(param)[var].count()
    err = (1.96 * df.groupby(param)[var].std()) / np.sqrt(replicates)
    ax.errorbar(x, y, yerr=err.as_matrix())

    ax.scatter(df[param], df[var])
    ax.set_xlabel(param)
    ax.set_ylabel(var)
    ax.set_ylim([-1, 1])


def plot_all_vars(df, param):
    f, axs = plt.subplots(3, figsize=(7, 10))
    plot_param_var(axs[0], df, param, 'pfl_net')
    plot_param_var(axs[1], df, param, 'pu_net')
    plot_param_var(axs[2], df, param, 'flu_net')


def read_data(path):
    data = pd.read_csv(path)
    data['total'] = np.round(data['N'] // 2) + np.round((data['N'] // 2) * data['ratio']) + data['N'] - np.round(
        data['N'] // 2) - np.round(
        (data['N'] // 2) * data['ratio'])

    data['pfl_net'] = (data['pheromone'] - data['followers'] - data['leaders']) / data['total']
    data['pu_net'] = (data['pheromone'] - data['unassigned']) / data['total']
    data['flu_net'] = (data['followers'] + data['leaders'] - data['unassigned']) / data['total']

    return data


if __name__ == '__main__':

    params = ['p_uf', 'p_pu', 'p_up', 'p_fl', 'p_lu', 'g', 'ratio', 'N', 'size']
    prefix = '../Data/ofat_full/ofat_2_2_2_'
    for param in params:
        data = read_data(prefix + param + '.csv')
        plot_all_vars(data, param)
    plt.show()
