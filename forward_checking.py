import time

from CSP import Csp

PRINT_THRESHOLD_INCREMENT = 100000

checked_nodes = 0
curr_print_threshold = PRINT_THRESHOLD_INCREMENT


def forward_check(blocks, grid_size, heuristic):
    return recursive_forward_check({}, Csp(blocks, grid_size, heuristic))


def recursive_forward_check(assignment, csp):
    global checked_nodes, curr_print_threshold, PRINT_THRESHOLD_INCREMENT
    
    if csp.is_complete(assignment):
        return assignment, checked_nodes
    
    var = csp.get_next_unassigned_var()

    #my_copy = {key: set(value) for key, value in csp.domains.items()}
    for value in csp.domains[var]:
        checked_nodes += 1
        if csp.is_consistent(value, assignment):
            csp.assign_val(var, value, assignment)
            removed_domains = {}  # for restore in case the assignment fails. using this eliminates unneccessary copy of unchanged domains
            no_wipeout = csp.propogate_constraints(value, removed_domains)
            if not no_wipeout:
                # there was a domain wipeout
                csp.unassign_val(var, value, assignment)
                #csp.domains = {key: set(value) for key, value in my_copy.items()}
                csp.restore_domains(removed_domains)
                continue
            result = recursive_forward_check(assignment, csp)
            if result:
                return result
            csp.unassign_val(var, value, assignment)
            csp.restore_domains(removed_domains)
            #csp.domains = {key: set(value) for key, value in my_copy.items()}
        if (time.time() - csp.start_time) / 60 >= 10:
            return None
    
    if checked_nodes >= curr_print_threshold:
        print('Checked {0} states so far'.format(checked_nodes))
        curr_print_threshold += PRINT_THRESHOLD_INCREMENT
    
    return None
