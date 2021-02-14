import math


def convert_string_to_grid_array(grid_string):
    blocks = []
    grid_size = int(math.sqrt(len(grid_string)))
    for i in range(grid_size):
        blocks.append([])

    for i, char in enumerate(grid_string):
        blocks[ord(char) - ord('A')].append(i + 1)
    return blocks, grid_size
