"""
    File name: grid_file_loader.py
    Author: Arsh Khokhar, Kiernan Wiese
    Date last modified: 22 February, 2021
    Python Version: 3.8

    This script contains a function to read a grid file located in the same
    folder as this script. It reads the file and returns a 2D list of blocks
    and the size of the grid, which are used in the csp algorithms to get the
    block constraints.
"""


def load_grid_file(name: str):
    """
    Reads grid file and loads data into a 2D array.

    :param name: The name of the grid file to be loaded.
    :return: 2D list of blocks, size of grid
    """

    blocks = []
    with open(name, 'r') as file:
        lines = file.readlines()
        for line in lines:
            cells = line.strip().split('\t')[1].split(',')
            # convert strings to ints
            blocks.append(sorted([int(numeric_string) for numeric_string in cells]))

    # The below retrieval assumes the format "gridNxN.txt".
    grid_size = name.split('grid')[-1].split('.')[0].split('x')

    return blocks, int(grid_size[0])
