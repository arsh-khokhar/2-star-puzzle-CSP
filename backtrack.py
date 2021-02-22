"""
    File name: backtrack.py
    Author: Arsh Khokhar, Kiernan Weise
    Date last modified: 22 February, 2021
    Python Version: 3.9

    This script contains the backtracking algorithm for solving the
    2-star constraint satisfaction problem. The algorithm can be
    called externally by calling the function backtrack, which takes
    the grid as a 2d array of blocks, the size of the grid, and the
    heuristic to be used as arguments.
"""

import time

from CSP import Csp

PRINT_THRESHOLD_INCREMENT = 100000

checked_nodes = 0
curr_print_threshold = PRINT_THRESHOLD_INCREMENT


def backtrack(blocks: list, grid_size: int, heuristic: int):
    """
    Constructs a new csp object and calls the recursive backtracking algorithm
    to solve the problem

    :param blocks: 2-D array containing the blocks, and their contents.
    :param grid_size: Size of the grid (10x10 grid -> 10)
    :param heuristic: The heuristic to be used for the algorithm
    :return: A valid solution of the 2-star csp
    """
    return recursive_backtrack({}, Csp(blocks, grid_size, heuristic))


def recursive_backtrack(assignment: set, csp: object):
    """
    Recursively attempts to solve the 2-star csp using backtracking
    :param assignment: Current assignment for the 2-star csp
    :param csp: 2-star csp object for the current recursion level
    :return assignment: A valid solution of the 2-star csp, if no solution, then return None
    :return checked_nodes: The number of nodes checked while attempting to find a solution
    """
    global checked_nodes, curr_print_threshold, PRINT_THRESHOLD_INCREMENT
    
    if csp.is_complete(assignment):
        return assignment, checked_nodes

    var = csp.get_next_unassigned_var() # csp object takes care of the heuristic check by itself
    
    for value in csp.domains[var]:
        checked_nodes += 1
        if csp.is_consistent(value, assignment):
            csp.assign_val(var, value, assignment) # adding to the assignment, updating other variables as required
            result = recursive_backtrack(assignment, csp)   # continue to next recusrion level
            if result:
                return result   # found a valid assignment
            csp.unassign_val(var, value, assignment) # deleting from the assignment
        # If the time taken is more than 10 mins, return no solution
        if (time.time() - csp.start_time) / 60 >= 10:
            return None, checked_nodes
    
    if checked_nodes >= curr_print_threshold:
        print('Checked {0} states so far'.format(checked_nodes))
        curr_print_threshold += PRINT_THRESHOLD_INCREMENT
    return None
