from model import Environment
import matplotlib.pyplot as plt
import numpy as np
from matplotlib import animation
import matplotlib.patches as patches
import itertools


def grid_to_array(pos, width, height):
    return pos[0] - 0.5, height - pos[1] - 1.5

"""
@def store_state

<<<<<<< HEAD
@param colony_positions
@param food_positions
@param ant_positions
@param ant_foods carries the boolean about whether an ant carries food or not
"""
def store_state(i, pheromones, colony_positions, food_positions, ant_positions, ant_foods, obstacle_positions):

    # append the pheromone distribution
    pheromones.append(np.rot90(np.copy(env.pheromones)))

    # append the positions of the colonies
    for j, colony in enumerate(env.colonies):
        for x, y in itertools.product(np.arange(-colony.radius, colony.radius + 1), np.arange(-colony.radius, colony.radius + 1)):
            pos = np.add(colony.pos, (x, y))
            if colony.on_colony(pos):
                colony_positions[i].append(grid_to_array(pos, width, height))

        # append the positions of the ants
        for k, agent in enumerate(colony.ant_list.agents):
            ant_positions[i].append(grid_to_array(agent.pos, width, height))
            ant_foods[i].append(agent.carry_food)

    for j, obstacle in enumerate(env.obstacles):
        obstacle_positions[i].append(grid_to_array(obstacle.pos, width, height))

    # append the positions of the food
    for x, y in np.array(np.where(env.food.grid > 0)).T:
        food_positions[i].append(grid_to_array((x, y), width, height))


def init_figure(pheromones, colony_positions, food_positions, ant_positions, ant_foods, obstacle_positions):
    fig = plt.figure()
    ax = fig.add_subplot(111)
    im = ax.imshow(np.zeros((width, height)), vmin=0, vmax=np.max([np.max(p) for p in pheromones]),
                   interpolation='None',
                   cmap="terrain_r")

    colony_patches, food_patches, ant_patches, obstacle_patches = [], [], [], []

    for colony_pos in colony_positions[0]:
        col = patches.Rectangle(colony_pos, 1, 1, linewidth=1, edgecolor='r', facecolor='r', fill=True)
        ax.add_patch(col)
        colony_patches.append(col)
    for food_pos in food_positions[0]:
        food = patches.Rectangle(food_pos, 1, 1, linewidth=1, edgecolor='g', facecolor='g', fill=True)
        ax.add_patch(food)
        food_patches.append(food)
    for ant_pos, ant_food in zip(ant_positions[0], ant_foods[0]):
        ant_pos = (ant_pos[0] + (1 - ant_size) / 2, ant_pos[1] + (1 - ant_size) / 2)
        ant = patches.Rectangle(ant_pos, ant_size, ant_size, linewidth=2, edgecolor='k', facecolor='k', fill=False)
        ax.add_patch(ant)
        ant_patches.append(ant)
    for obstacle_pos in obstacle_positions[0]:
        obs = patches.Rectangle(obstacle_pos, 1, 1, linewidth= 1, edgecolor='magenta', facecolor='magenta', fill=True)
        ax.add_patch(obs)
        obstacle_patches.append(obs)

    return fig, ax, im, colony_patches, food_patches, ant_patches, obstacle_patches

# <<<<<<< HEAD
#
# def animate(i):
#     im.set_array(pheromones[i].astype(np.float64).reshape(width, height))  # update the data
#     for j, colony_patch in enumerate(colony_patches):
#         colony_patch.set_xy(colony_positions[i][j])
#     for j, food_patch in enumerate(food_patches):
#         food_patch.set_xy(food_positions[i][j])
#     for j, ant_patch in enumerate(ant_patches):
#         ant_pos = ant_positions[i][j]
#         ant_pos = (ant_pos[0] + (1 - ant_size) / 2, ant_pos[1] + (1 - ant_size) / 2)
#         ant_patch.set_xy(ant_pos)
#         if ant_foods[i][j]:
#             ant_patch.set_facecolor('g')
#             ant_patch.set_edgecolor('g')
#             ant_patch.set_fill(True)
#         else:
#             ant_patch.set_facecolor('k')
#             ant_patch.set_edgecolor('k')
#             ant_patch.set_fill(False)
#     plt.title('iteration: ' + str(i))
#     fig.canvas.draw()
#     return im
#
#
# env = Environment(width=width, height=height, n_colonies=1, n_ants=100, n_obstacles=10, decay=0.99, sigma=0.2, moore=True)
#
# pheromones = []
# ant_positions = [[] for _ in range(steps + 1)]
# colony_positions = [[] for _ in range(steps + 1)]
# food_positions = [[] for _ in range(steps + 1)]
# ant_foods = [[] for _ in range(steps + 1)]
# obstacle_positions = [[] for _ in range(steps + 1)]
# store_state(0, colony_positions, food_positions, ant_positions, ant_foods, obstacle_positions)
# for i in range(1, steps + 1):
#     # take a step
#     env.step()
#
#     # store the state for animation
#     store_state(i, colony_positions, food_positions, ant_positions, ant_foods, obstacle_positions)
#
#
# fig, ax, im, colony_patches, food_patches, ant_patches, obstacle_positions = init_figure()
# ani = animation.FuncAnimation(fig, animate, steps, interval=1)
# plt.figure()
# plt.plot(env.path_lengths)
# plt.show()
#
# =======
def compute_then_plot(env, steps):
    pheromones = []
    ant_positions = [[] for _ in range(steps + 1)]
    colony_positions = [[] for _ in range(steps + 1)]
    food_positions = [[] for _ in range(steps + 1)]
    ant_foods = [[] for _ in range(steps + 1)]
    obstacle_positions = [[] for _ in range(steps + 1)]

    store_state(0, pheromones, colony_positions, food_positions, ant_positions, ant_foods, obstacle_positions)
    for i in range(1, steps + 1):
        # take a step
        env.step()

        # store the state for animation
        store_state(i, pheromones, colony_positions, food_positions, ant_positions, ant_foods, obstacle_positions)

    fig, ax, im, colony_patches, food_patches, ant_patches, obstacle_patches = init_figure(pheromones, colony_positions, food_positions, ant_positions, ant_foods, obstacle_positions)

    def animate(i):
        im.set_array(pheromones[i].astype(np.float64).reshape(width, height))  # update the data
        for j, colony_patch in enumerate(colony_patches):
            colony_patch.set_xy(colony_positions[i][j])
        for j, food_patch in enumerate(food_patches):
            food_patch.set_xy(food_positions[i][j])
        for j, ant_patch in enumerate(ant_patches):
            ant_pos = ant_positions[i][j]
            ant_pos = (ant_pos[0] + (1 - ant_size) / 2, ant_pos[1] + (1 - ant_size) / 2)
            ant_patch.set_xy(ant_pos)
            if ant_foods[i][j]:
                ant_patch.set_facecolor('g')
                ant_patch.set_edgecolor('g')
                ant_patch.set_fill(True)
            else:
                ant_patch.set_facecolor('k')
                ant_patch.set_edgecolor('k')
                ant_patch.set_fill(False)
        plt.title('iteration: ' + str(i))
        fig.canvas.draw()
        return im

    ani = animation.FuncAnimation(fig, animate, steps, interval=1)
    plt.figure()
    plt.plot(env.min_path_lengths)
    plt.ylim(ymin=0)
    plt.show()

def plot_continuous(env, steps = 1000):
    pheromones = []

    ant_positions = [[] for _ in range(steps + 1)]
    colony_positions = [[] for _ in range(steps + 1)]
    food_positions = [[] for _ in range(steps + 1)]
    ant_foods = [[] for _ in range(steps + 1)]
    obstacle_positions = [[] for _ in range(steps + 1)]

    store_state(0, pheromones, colony_positions, food_positions, ant_positions, ant_foods, obstacle_positions)

    fig, ax, im, colony_patches, food_patches, ant_patches, obstacle_patches = init_figure(pheromones, colony_positions, food_positions, ant_positions, ant_foods, obstacle_positions)

    im = ax.imshow(np.zeros((width, height)), vmin=0, vmax=100,
                       interpolation='None',
                       cmap="Purples")


    plt.ion()
    fig.show()

    for i in range(steps):
        plt.title('iteration: ' + str(i))
        plt.pause(0.001)

        # take a step
        env.step()

        # store the state for animation
        store_state(i + 1, pheromones, colony_positions, food_positions, ant_positions, ant_foods, obstacle_positions)

        im.set_array(pheromones[i].astype(np.float64).reshape(width, height))  # update the data
        for j, colony_patch in enumerate(colony_patches):
            colony_patch.set_xy(colony_positions[i][j])
        for j, food_patch in enumerate(food_patches):
            food_patch.set_xy(food_positions[i][j])
        for j, ant_patch in enumerate(ant_patches):
            ant_pos = ant_positions[i][j]
            ant_pos = (ant_pos[0] + (1 - ant_size) / 2, ant_pos[1] + (1 - ant_size) / 2)
            ant_patch.set_xy(ant_pos)
            if ant_foods[i][j]:
                ant_patch.set_facecolor('g')
                ant_patch.set_edgecolor('g')
                ant_patch.set_fill(True)
            else:
                ant_patch.set_facecolor('k')
                ant_patch.set_edgecolor('k')
                ant_patch.set_fill(False)

        fig.canvas.draw()

if __name__ == '__main__':
    width = 20
    height = 20
    steps = 200
    ant_size = 0.4

    env = Environment(width=width, height=height, n_colonies=1, n_ants=100, n_obstacles=10, decay=0.99, sigma=0.2, moore=True)

    # compute_then_plot(env, steps)
    plot_continuous(env, steps=steps)

