from CSP import Csp
from Examples.StringToGridArray import convert_string_to_grid_array
from GridDisplay import display_grid
import time

checked_nodes = 0
curr_print_threshold = 0
PRINT_THRESHOLD_INCREMENT = 100000

def backtrack(blocks, grid_size, heuristic):
    return recursive_backtrack({}, Csp(blocks, grid_size, heuristic))

def recursive_backtrack(assignment, csp):
    global checked_nodes, curr_print_threshold, PRINT_THRESHOLD_INCREMENT
    
    if csp.is_complete(assignment):
        return assignment

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

# blocks = [[1, 11, 21, 22], 
# [2, 3, 4, 12, 13, 14, 23, 24, 31, 32, 33, 34, 44, 45, 46, 53, 54, 64], 
# [5, 15, 25, 26, 35, 36], 
# [6, 7, 8, 16, 17, 27, 28, 29, 37, 38, 39, 49, 50, 59, 60, 69, 70], 
# [9, 10, 18, 19, 20, 30, 40], 
# [41, 42, 43, 51], 
# [47, 48, 55, 56, 57, 65, 66, 67, 76, 86], 
# [52, 61, 62, 63, 71, 72, 73, 74, 75, 81, 82, 83, 84, 85, 91, 92, 93, 94, 95, 96], 
# [58, 68, 77, 78], 
# [79, 80, 87, 88, 89, 90, 97, 98, 99, 100]]

# grid_size = 10

# blocks, grid_size = convert_string_to_grid_array('ABBBCDDDEEABBBCDDEEEAABBCCDDD'
#                                                  'EBBBBCCDDDEFFFBBBGGDDFHBBGGGI'
#                                                  'DDHHHBGGGIDDHHHHHGIIJJHH'
#                                                  'HHHGJJJJHHHHHHJJJJ')

# temporary test code, will be moved eventually
blocks, grid_size = convert_string_to_grid_array('AAABBBBBBBBDDD'
                                                 'AAAHHBCBCCCCDD'
                                                 'HHHHHECCCFFCDD'
                                                 'HHHEEEEECFCCCD'
                                                 'HHHGGEEFCFCCDD'
                                                 'HHHGGGEFFFCFDD'
                                                 'IHHHGGFFHFFFFD'
                                                 'IIHHGHHHHJJJFD'
                                                 'IIHHHHHKHHHJJJ'
                                                 'INNNHKKKLJJJLJ'
                                                 'IINNHMMKLJJLLJ'
                                                 'IINHHHMMLJJJLJ'
                                                 'IHHHMMMMLLLLLJ'
                                                 'IIHHHMMMMLLLLL')

start_time = time.time()

# heuristic will come from args or something similar
heuristic = 2

csp_assignment = backtrack(blocks, grid_size, heuristic)

end_time = time.time() - start_time
if not csp_assignment:
    print("\nNo solution found!")
    print("\nChecked {} nodes".format(checked_nodes))
    print("Evaluation took {} seconds ({} minutes {} seconds)".format(end_time, int(end_time // 60), end_time % 60))
else:
    print("\nSolution Found!")
    print("\nChecked {} nodes".format(checked_nodes))
    print("Evaluation took {} seconds ({} minutes {} seconds)".format(end_time, int(end_time // 60), end_time % 60))
    display_grid(blocks, grid_size, csp_assignment.values(), False, False)