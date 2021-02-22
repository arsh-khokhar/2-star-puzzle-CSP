import sys
import time

from backtrack import backtrack
from grid_display import display_grid
from grid_file_loader import load_grid_file
from forward_checking import forward_check


# TODO: unsure if we should have a main file or copy this code into both
#  backtrack.py and forward_checking.py, given the assignment description
def main():
    if len(sys.argv) < 4:
        print('Usage: python main.py [fc or bc] [grid file] [heuristic type (0,1,2,or 3)]')
        return -1
        # TODO: we might not specify the grid file, just read all 3 and output all solutions
        #  I've added code to do this, but feel free to remove it

    blocks, grid_size = load_grid_file(sys.argv[1])
    # blocks2, grid_size2 = load_grid_file('grid10x10.txt')
    # blocks3, grid_size3 = load_grid_file('grid14x14.txt')

    # test grid stuff goes here

    csp_assignment = {}
    start_time = time.time()
    checked_nodes = 0
    if sys.argv[2].lower() == 'bt':
        csp_assignment, checked_nodes = backtrack(blocks, grid_size, int(sys.argv[3]))
        # csp_assignment2, checked_nodes2 = backtrack(blocks2, grid_size2, int(sys.argv[3]))
        # csp_assignment3, checked_nodes3 = backtrack(blocks3, grid_size3, int(sys.argv[3]))
    elif sys.argv[2].lower() == 'fc':
        csp_assignment, checked_nodes = forward_check(blocks, grid_size, int(sys.argv[3]))
        # csp_assignment2, checked_nodes2 = forward_check(blocks2, grid_size2, int(sys.argv[3]))
        # csp_assignment3, checked_nodes3 = forward_check(blocks3, grid_size3, int(sys.argv[3]))

    end_time = time.time() - start_time
    if not csp_assignment:
        print("\nNo solution found!")
        print("\nChecked {} nodes".format(checked_nodes))
        # TODO: technically, we don't need to print time taken in the handin version,
        #  but we still need it for the report
        print("Evaluation took {} seconds ({} minutes {} seconds)".format(end_time, int(end_time // 60),
                                                                          end_time % 60))
        # TODO: do we need to print the grid if there's no solution?
        display_grid(blocks, grid_size, [])
    else:
        print("\nSolution Found!")
        print("\nChecked {} nodes".format(checked_nodes))
        # print("\nChecked {} nodes for 10x10".format(checked_nodes))
        # print("\nChecked {} nodes for 14x14".format(checked_nodes))
        print("Evaluation took {} seconds ({} minutes {} seconds)".format(end_time, int(end_time // 60),
                                                                          end_time % 60))
        display_grid(blocks, grid_size, csp_assignment.values())
        # display_grid(blocks2, grid_size2, csp_assignment2.values(), blocking=False, title='Solution 10x10')
        # display_grid(blocks3, grid_size3, csp_assignment3.values(), title='Solution 14x14')


if __name__ == '__main__':
    main()
