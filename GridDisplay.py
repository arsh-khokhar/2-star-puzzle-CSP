import matplotlib.pyplot as plt
import matplotlib.widgets as widgets
from math import floor
import numpy as np


def display_grid(blocks: list, grid_length: int, star_locs: list = None,
                 show_block_ids: bool = False, show_ids: bool = False):
    """
    Displays a grid, with thick lines separating blocks. Optionally, can show
    stars, block ids, and/or position ids.

    :param blocks: 2-D array containing the blocks, and their contents.
    :param grid_length: Size of the grid (10x10 grid -> 10)
    :param star_locs: Locations of stars.
    :param show_block_ids: Show block id within each grid position.
    :param show_ids: Show position ids within each position.
    :return: Opens a new window to display the grid.
    """

    # Create figure and axes
    fig, ax = plt.subplots()

    # create grid
    for x in range(grid_length + 1):
        ax.axhline(x, lw=2, color='c')
        ax.axvline(x, lw=2, color='c')

    # create bolder borders around grid
    for x in (0, grid_length):
        ax.axhline(x, lw=8, color='k')
        ax.axvline(x, lw=8, color='k')
    
    ax.axvline(x, lw=2, color='k')
    for blockNum, block in enumerate(blocks):
        for cell in block:
            if show_block_ids:
                plt.text((cell - 1) % grid_length + 0.8,
                         floor((cell - 1) / grid_length) + 0.5,
                         blockNum + 1)
            if show_ids:
                plt.text((cell - 1) % grid_length + 0.1,
                         floor((cell - 1) / grid_length) + 0.5,
                         cell)

            if star_locs and cell in star_locs:
                star = plt.text((cell - 1) % grid_length + 0.5,
                                floor((cell - 1) / grid_length) + 0.5,
                                '★')
                star.set_fontsize('xx-large')
                star.set_horizontalalignment('center')
                star.set_verticalalignment('center')

            # we do 1 - (value) here due to the y-axis flip
            # since the lines aren't flipped during that operation
            y_min = 1 - floor((cell - 1) / grid_length) / grid_length
            y_max = 1 - (floor((cell - 1) / grid_length) + 1) / grid_length

            x_min = ((cell - 1) % grid_length) / grid_length
            x_max = ((cell - 1) % grid_length + 1) / grid_length

            # right line
            if cell % grid_length == 0 or cell+1 not in block:
                ax.axvline((cell - 1) % grid_length + 1, lw=4,
                           ymin=y_min, ymax=y_max, color='k')
            # left line
            if cell % grid_length == 1 or cell-1 not in block:
                ax.axvline((cell - 1) % grid_length, lw=4,
                           ymin=y_min, ymax=y_max, color='k')
            # above line
            if cell - grid_length not in block:
                ax.axhline(floor((cell - 1) / grid_length), lw=4,
                           xmin=x_min, xmax=x_max, color='k')
            # below line
            if cell + grid_length not in block:
                ax.axhline(floor((cell - 1) / grid_length) + 1, lw=4,
                           xmin=x_min, xmax=x_max, color='k')

    plt.xlim([0, grid_length])
    plt.ylim([0, grid_length])

    # this is done so that 0,0 is the top-left (default is bottom-left)
    ax = plt.gca()  # get the axis
    ax.set_ylim(ax.get_ylim()[::-1])  # invert the axis
    ax.xaxis.tick_top()  # and move the X-Axis
    ax.yaxis.set_ticks(np.arange(0, 5, 1))  # set y-ticks
    ax.yaxis.tick_left()  # remove right y-Ticks

    ax.axis('off')
    
    plt.show()
