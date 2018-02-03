# -*- coding: utf-8 -*-
"""
Implements the various matplotlib plots for this project.
"""
import matplotlib.pyplot as plt
import numpy as np
from itertools import product
import pandas as pd
from IPython import display
import matplotlib.patches as patches

from model import Environment
from roles import Unassigned, Follower, Leader, Pheromone


def plot_p_fl(df):
    """
    Creates (and shows) the p vs (f + l) plot.

    Args:
        df: the dataframe containing 'pheromone', 'followers', and 'leaders'
    """
    plt.figure()
    plt.scatter(df['pheromone'], df['followers'] + df['leaders'])
    plt.xlabel(r'$p$')
    plt.ylabel(r'$f + l$')
    plt.show()


def plot_col(df, cols):
    """
    Plots the variables in the cols list.

    Args:
        df: the dataframe containing entries from cols
        cols: list containing the dict entries to be plotted.
    """
    plt.figure()
    df[cols].plot()
    plt.show()


def plot_continuous(env, steps=1000):
    """
    Shows the passed environment over time. Terminates gracefully when closing
    the animation window.

    Args:
        env: the environment to be shown
        steps (int): the amount of steps to animate (default 1000)
    """
    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.set_xlim([0, env.width])
    ax.set_ylim([0, env.height])
    env.animate(ax)
    fig_num = plt.get_fignums()[0]
    custom_patches = [
        patches.Rectangle((0, 0), 0.4, 0.4, linewidth=2, edgecolor='k', facecolor='g', fill=True, zorder=2),
        patches.Rectangle((0, 0), 0.4, 0.4, linewidth=2, edgecolor='k', facecolor='r', fill=True, zorder=2),
        patches.Rectangle((0, 0), 0.4, 0.4, linewidth=2, edgecolor='k', facecolor='b', fill=True, zorder=2),
        patches.Rectangle((0, 0), 0.4, 0.4, linewidth=2, edgecolor='k', facecolor='c', fill=True, zorder=2)]
    ax.legend(custom_patches, ['Unassigned', 'Follower', 'Leader', 'Pheromoner'], loc='center left', bbox_to_anchor=(1, 0.5))
    for i in range(steps):
        if not plt.fignum_exists(fig_num): break

        plt.title('iteration: ' + str(i))
        plt.pause(0.001)

        # Take a step
        env.step()

        # Store the state for animation
        env.animate(ax)
        fig.canvas.draw()



def plot_continuous_notebook(env, steps=1000):
    """
    Shows the passed environment over time. Terminates gracefully when closing
    the animation window.

    Args:
        env: the environment to be shown
        steps (int): the amount of steps to animate (default 1000)
    """
    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.set_xlim([0, env.width])
    ax.set_ylim([0, env.height])
    env.animate(ax)
    fig_num = plt.get_fignums()[0]
    custom_patches = [
        patches.Rectangle((0, 0), 0.4, 0.4, linewidth=2, edgecolor='k', facecolor='g', fill=True, zorder=2),
        patches.Rectangle((0, 0), 0.4, 0.4, linewidth=2, edgecolor='k', facecolor='r', fill=True, zorder=2),
        patches.Rectangle((0, 0), 0.4, 0.4, linewidth=2, edgecolor='k', facecolor='b', fill=True, zorder=2),
        patches.Rectangle((0, 0), 0.4, 0.4, linewidth=2, edgecolor='k', facecolor='c', fill=True, zorder=2)]
    ax.legend(custom_patches, ['Unassigned', 'Follower', 'Leader', 'Pheromoner'], loc='center left', bbox_to_anchor=(1, 0.5))

    display.clear_output(wait=True)
    display.display(plt.gcf())

    for i in range(steps):
        if not plt.fignum_exists(fig_num): break

        plt.title('iteration: ' + str(i))
        plt.pause(0.001)

        # Take a step
        env.step()

        # Store the state for animation
        env.animate(ax)
        fig.canvas.draw()

        # Flush display
        display.clear_output(wait=True)
        display.display(plt.gcf())


def plot_param_var(ax, df, param, var):
    x = df.groupby(param).mean().reset_index()[param]
    y = df.groupby(param).mean()[var]
    replicates = df.groupby(param)[var].count()
    err = (1.96 * df.groupby(param)[var].std()) / np.sqrt(replicates)
    ax.errorbar(x, y, yerr=err.as_matrix())

    ax.scatter(df[param], df[var])
    ax.set_xlabel(param)
    ax.set_ylabel(var)
    ax.set_ylim([-1.1, 1.1])


def plot_all_vars(df, param):
    f, axs = plt.subplots(3, figsize=(7, 10))
    plot_param_var(axs[0], df, param, 'pfl_net')
    plot_param_var(axs[1], df, param, 'pu_net')
    plot_param_var(axs[2], df, param, 'flu_net')


def plot_index(s, params, i, title=''):
    if i == '2':
        params = list(product(params))
    indices = s['S' + i]
    errors = s['S' + i + '_conf']
    l = len(indices)
    plt.figure()
    plt.title(title)
    plt.ylim([-0.2, len(indices) - 1 + 0.2])
    plt.yticks(range(l), params)
    plt.errorbar(indices, range(l), xerr=errors, linestyle='None', marker='o')
    plt.axvline(0, c='k')
