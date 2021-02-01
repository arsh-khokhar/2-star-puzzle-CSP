
def load_grid_file(name):
    """
    Reads grid file and loads data into a 2D array.

    TODO: This is very basic, we'll likely need verification or to keep track
    of other things as we progress

    :param name: The name of the grid file to be loaded.
    :return: 2D array of blocks
    """

    blocks = []
    with open(name, 'r') as file:
        lines = file.readlines()
        for line in lines:
            cells = line.strip().split('\t')[1].split(',')
            # convert strings to ints
            blocks.append([int(numeric_string) for numeric_string in cells])
    print(blocks)
    return blocks

# TODO: use a gui instead
def print_grid(grid):
    """
    Print a grid in ascii.

    :param grid: To be changed, since we need to print stars.
    """
    for x in range(5):
        print('_', end='')
    print()

    for x in range(5):
        print('_', end='')
    print()


if __name__ == '__main__':
    grid = load_grid_file('grid5x5.txt')
    print_grid(grid)

# my attempt at an assci art table (a gui is probably a better idea)
"""
_____
| |*|  
|_|_|
|   |
_____
"""
