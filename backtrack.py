from csp import Csp
from Examples.StringToGridArray import convert_string_to_grid_array
from GridDisplay import display_grid
import time

checked_nodes = 0

def backtrack(blocks, grid_size):
    return recursive_backtrack({}, Csp(blocks, grid_size))

def recursive_backtrack(assignment, csp):
    global checked_nodes
    
    if csp.is_complete(assignment):
        return assignment
    
    var = csp.get_next_unassigned_var()
    for value in csp.domains[var]:
        checked_nodes += 1
        if csp.is_consistent(value, assignment):
            csp.assign_val(var, value, assignment) #assignment[var] = value
            result = recursive_backtrack(assignment, csp)
            if result:
                return result
            csp.unassign_val(var, value, assignment) # deleting from the assignment
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

csp_assignment = backtrack(blocks, grid_size)

if not csp_assignment:
    print("\nNo solution found!")
else:
    print("\nSolution Found!")
    print("\nChecked {} nodes".format(checked_nodes))
    print("Evaluation took {} seconds".format(time.time() - start_time))
    display_grid(blocks, grid_size, csp_assignment.values(), False, False)