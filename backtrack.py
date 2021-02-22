import time

from CSP import Csp

PRINT_THRESHOLD_INCREMENT = 100000

checked_nodes = 0
curr_print_threshold = PRINT_THRESHOLD_INCREMENT


def backtrack(blocks, grid_size, heuristic):
    return recursive_backtrack({}, Csp(blocks, grid_size, heuristic))


def recursive_backtrack(assignment, csp):
    global checked_nodes, curr_print_threshold, PRINT_THRESHOLD_INCREMENT
    
    if csp.is_complete(assignment):
        return assignment, checked_nodes

    var = csp.get_next_unassigned_var()
    
    for value in csp.domains[var]:
        checked_nodes += 1
        if csp.is_consistent(value, assignment):
            csp.assign_val(var, value, assignment) #assignment[var] = value
            removed_domains = None
            if csp.ordering_choice > 0:
                removed_domains = {}
                csp.propogate_constraints(value, removed_domains)
            result = recursive_backtrack(assignment, csp)
            if result:
                return result
            csp.unassign_val(var, value, assignment) # deleting from the assignment
            if csp.ordering_choice > 0:
                csp.restore_domains(removed_domains)
        if (time.time() - csp.start_time) / 60 >= 10:
            return None
    
    if checked_nodes >= curr_print_threshold:
        print('Checked {0} states so far'.format(checked_nodes))
        curr_print_threshold += PRINT_THRESHOLD_INCREMENT
    return None
