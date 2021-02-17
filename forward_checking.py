from copy import copy, deepcopy
from GridDisplay import display_grid
from CSP import Csp
from Examples.StringToGridArray import convert_string_to_grid_array
import datetime

total_states = 0
curr_print_threshold = 0
PRINT_THRESHOLD_INCREMENT = 100000


def forward_check(blocks: list, grid_size: int):
    """
    Helper method for recursive_backtracking_search

    :param blocks: 2D array representing the blocks of the grid
    :param grid_size: Size of the grid (10x10 grid -> 10)
    :return: The csp containing a solution if there is one, None otherwise
    """
    global total_states, curr_print_threshold
    total_states = 0
    curr_print_threshold = PRINT_THRESHOLD_INCREMENT
    start = datetime.datetime.now()
    result = recursive_forward_check(Csp(grid_size, blocks))
    end = datetime.datetime.now()
    print('\nEvaluation took: {0}'.format(end - start))
    return result


def recursive_forward_check(csp: Csp):
    """
    Implements backtracking search to solve a given Constraint Satisfaction
    Problem

    :param csp: CSP object
    :return: The csp containing a solution if there is one, None otherwise
    """
    global total_states, curr_print_threshold
    if csp.complete_csp:
        return csp

    domains_copy = [x[:] for x in csp.star_domains] # to make a deepcopy of the stuff
    curr = csp.next_star_to_assign
    for value in csp.star_domains[curr]:
        total_states += 1
        if csp.is_valid(value):
            csp.assign_value(curr, value)
            # need to check if there was a domain wipeout
            if not csp.propogate_constraints(curr):
               csp.star_domains = [x[:] for x in domains_copy]
               csp.unassign_value(curr)
               return None
            result = recursive_forward_check(csp)
            if result:
                return result
            csp.star_domains = [x[:] for x in domains_copy] # to make a deepcopy of the stuff
            csp.unassign_value(curr)
            
    if total_states >= curr_print_threshold:
        print('Checked {0} states so far'.format(total_states))
        curr_print_threshold += PRINT_THRESHOLD_INCREMENT
    return None


# temporary test code, will be moved eventually
grid, grid_length = convert_string_to_grid_array('ABBBCDDDEEABBBCDDEEEAABBCCDDD'
                                                 'EBBBBCCDDDEFFFBBBGGDDFHBBGGGI'
                                                 'DDHHHBGGGIDDHHHHHGIIJJHH'
                                                 'HHHGJJJJHHHHHHJJJJ')

csp = forward_check(grid, grid_length)
if csp:
    print('\nSolution found!')
    print('\nStar positions: {0}'.format(csp.star_values))
    print('Number of states checked: {0}'.format(total_states))
    display_grid(grid, grid_length, csp.star_values)
else:
    print('no solution found')
