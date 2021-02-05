from GridDisplay import display_grid
from Csp import Csp2Star

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
    

    # The below retrival assumes the format "gridNxN.txt". Need to add error handling later

    grid_size = name.split('grid')[-1].split('.')[0].split('x') # retrive size of the grid from the filename
    assert(grid_size[0] == grid_size[-1]) # we only support square grids, so this check is required
    return blocks, int(grid_size[0])

if __name__ == '__main__':
    grid, grid_length = load_grid_file('grid8x8.txt')
    csp = Csp2Star(len(grid), grid_length)
    print()
    print(len(csp.nodes))
    
    for node in csp.nodes:
        print(node.id)
    display_grid(grid, grid_length, [1,2,9,10,20,21,28,29,38,39,46,47,49,50,57,58],
                 show_block_ids=True, show_ids=True)

