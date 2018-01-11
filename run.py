from model import Environment
import matplotlib.pyplot as plt
import numpy as np
from matplotlib import animation
import matplotlib.patches as patches


width = 10
height = 10
steps = 1000
ant_size = 0.4


def grid_to_array(pos, width, height):
    return pos[0] - 0.5, height - pos[1] - 1.5


def store_state(i, colony_positions, food_positions, ant_positions, ant_foods):
    # append the pheromone distribution
    pheromones.append(np.rot90(np.copy(env.pheromones)))

    # append the positions of the colonies
    for j, colony in enumerate(env.colonies):
        # colony_positions[i].append(np.abs(list(map(operator.sub, [0, height], env.colonies[0].pos))))
        colony_positions[i].append(grid_to_array(colony.pos, width, height))

        # append the positions of the ants
        for k, agent in enumerate(colony.ant_list.agents):
            ant_positions[i].append(grid_to_array(agent.pos, width, height))
            ant_foods[i].append(agent.carry_food)

    # append the positions of the food
    for x, y in np.array(np.where(env.food.grid > 0)).T:
        food_positions[i].append(grid_to_array((x, y), width, height))

def init_figure():
    fig = plt.figure()
    ax = fig.add_subplot(111)
    im = ax.imshow(np.zeros((width, height)), vmin=0, vmax=np.max([np.max(p) for p in pheromones]), interpolation='none',
                   cmap="Purples")

    colony_patches, food_patches, ant_patches = [], [], []

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

    return fig, ax, im, colony_patches, food_patches, ant_patches


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


env = Environment(width=width, height=height, n_colonies=1, n_ants=10, decay=0.99)

pheromones = []
ant_positions = [[] for _ in range(steps + 1)]
colony_positions = [[] for _ in range(steps + 1)]
food_positions = [[] for _ in range(steps + 1)]
ant_foods = [[] for _ in range(steps + 1)]
store_state(0, colony_positions, food_positions, ant_positions, ant_foods)
for i in range(1, steps + 1):
    # take a step
    env.step()

    # store the state for animation
    store_state(i, colony_positions, food_positions, ant_positions, ant_foods)


fig, ax, im, colony_patches, food_patches, ant_patches = init_figure()
ani = animation.FuncAnimation(fig, animate, steps, interval=1)
plt.show()

