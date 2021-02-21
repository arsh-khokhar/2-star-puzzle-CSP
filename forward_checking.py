from csp import Csp
from Examples.StringToGridArray import convert_string_to_grid_array
from GridDisplay import display_grid
import time

checked_nodes = 0
curr_print_threshold = 0
PRINT_THRESHOLD_INCREMENT = 100000

def forward_check(blocks, grid_size):
    return recursive_forward_check({}, Csp(blocks, grid_size))

def recursive_forward_check(assignment, csp):
    global checked_nodes, curr_print_threshold, PRINT_THRESHOLD_INCREMENT
    
    if csp.is_complete(assignment):
        return assignment
    
    var = csp.get_next_unassigned_var()
    #var = csp.get_most_constrained() #get_next_unassigned_var()

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
                return None
            result = recursive_forward_check(assignment, csp)
            if result:
                return result
            csp.unassign_val(var, value, assignment)
            csp.restore_domains(removed_domains)
            #csp.domains = {key: set(value) for key, value in my_copy.items()}
    
    if checked_nodes >= curr_print_threshold:
        print('Checked {0} states so far'.format(checked_nodes))
        curr_print_threshold += PRINT_THRESHOLD_INCREMENT
    
    return None

blocks, grid_size = convert_string_to_grid_array('ABBBCDDDEEABBBCDDEEEAABBCCDDD'
                                                 'EBBBBCCDDDEFFFBBBGGDDFHBBGGGI'
                                                 'DDHHHBGGGIDDHHHHHGIIJJHH'
                                                 'HHHGJJJJHHHHHHJJJJ')

# temporary test code, will be moved eventually
# blocks, grid_size = convert_string_to_grid_array('AAABBBBBBBBDDD'
#                                                  'AAAHHBCBCCCCDD'
#                                                  'HHHHHECCCFFCDD'
#                                                  'HHHEEEEECFCCCD'
#                                                  'HHHGGEEFCFCCDD'
#                                                  'HHHGGGEFFFCFDD'
#                                                  'IHHHGGFFHFFFFD'
#                                                  'IIHHGHHHHJJJFD'
#                                                  'IIHHHHHKHHHJJJ'
#                                                  'INNNHKKKLJJJLJ'
#                                                  'IINNHMMKLJJLLJ'
#                                                  'IINHHHMMLJJJLJ'
#                                                  'IHHHMMMMLLLLLJ'
#                                                  'IIHHHMMMMLLLLL')

start_time = time.time()

csp_assignment = forward_check(blocks, grid_size)

if not csp_assignment:
    print("\nNo solution found!")
    print("\nChecked {} nodes".format(checked_nodes))
    print("Evaluation took {} seconds".format(time.time() - start_time))
else:
    print("\nSolution Found!")
    print("\nChecked {} nodes".format(checked_nodes))
    print("Evaluation took {} seconds".format(time.time() - start_time))
    display_grid(blocks, grid_size, csp_assignment.values(), False, False)