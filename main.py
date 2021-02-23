import sys
import time

from backtrack import backtrack
from grid_display import display_grid
from grid_file_loader import load_grid_file
from forward_checking import forward_check


def main():
    if len(sys.argv) < 3:
        print('Usage: python main.py [fc or bt] [heuristic type (0,1,2,or 3)]')
        return -1

    blocks_8x8, grid_size_8x8 = load_grid_file('grid8x8.txt')
    blocks_10x10, grid_size_10x10 = load_grid_file('grid10x10.txt')
    blocks_14x14, grid_size_14x14 = load_grid_file('grid14x14.txt')

    csp_assignment_8x8 = {}
    checked_nodes_8x8 = 0
    solution_8x8 = None
    csp_assignment_10x10 = {}
    checked_nodes_10x10 = 0
    solution_10x10 = None
    csp_assignment_14x14 = {}
    checked_nodes_14x14 = 0
    solution_14x14 = None

    start_time = time.time()
    if sys.argv[1].lower() == 'bt':
        solution_8x8 = backtrack(blocks_8x8, grid_size_8x8, int(sys.argv[2]))
        solution_10x10 = backtrack(blocks_10x10, grid_size_10x10,
                                   int(sys.argv[2]))
        solution_14x14 = backtrack(blocks_14x14, grid_size_14x14,
                                   int(sys.argv[2]))
    elif sys.argv[1].lower() == 'fc':
        solution_8x8 = forward_check(blocks_8x8, grid_size_8x8,
                                     int(sys.argv[2]))
        solution_10x10 = forward_check(blocks_10x10, grid_size_10x10,
                                       int(sys.argv[2]))
        solution_14x14 = forward_check(blocks_14x14, grid_size_14x14,
                                       int(sys.argv[2]))

    if solution_8x8:
        csp_assignment_8x8, checked_nodes_8x8 = solution_8x8
    if solution_10x10:
        csp_assignment_10x10, checked_nodes_10x10 = solution_10x10
    if solution_14x14:
        csp_assignment_14x14, checked_nodes_14x14 = solution_14x14

    end_time = time.time() - start_time
    print("Evaluation took {} seconds ({} minutes {} seconds)"
          .format(end_time, int(end_time // 60), end_time % 60))

    print("\nChecked {} nodes for 8x8 grid".format(checked_nodes_8x8))
    if not csp_assignment_8x8:
        print("No solution found for 8x8 grid")
        display_grid(blocks_8x8, grid_size_8x8, [],
                     title='No solution found 8x8', blocking=False)
    else:
        print("Solution found for 8x8 grid")
        display_grid(blocks_8x8, grid_size_8x8, csp_assignment_8x8.values(),
                     title='Solution 8x8', blocking=False)

    print("\nChecked {} nodes for 10x10 grid".format(checked_nodes_10x10))
    if not csp_assignment_10x10:
        print("No solution found for 10x10 grid")
        display_grid(blocks_10x10, grid_size_10x10, [],
                     title='No solution found 10x10', blocking=False)
    else:
        print("Solution found for 10x10 grid")
        display_grid(blocks_10x10, grid_size_10x10,
                     csp_assignment_10x10.values(),
                     title='Solution 10x10', blocking=False)

    print("\nChecked {} nodes for 14x14 grid".format(checked_nodes_14x14))
    if not csp_assignment_14x14:
        print("No solution found for 14x14 grid")
        display_grid(blocks_14x14, grid_size_14x14, [],
                     title='No solution found 14x14')
    else:
        print("Solution found for 14x14 grid")
        display_grid(blocks_14x14, grid_size_14x14,
                     csp_assignment_14x14.values(),
                     title='Solution 14x14')


if __name__ == '__main__':
    main()
