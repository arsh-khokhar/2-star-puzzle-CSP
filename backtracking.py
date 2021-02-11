from main import load_grid_file
from GridDisplay import display_grid
from Assignment import Assignment


def backtracking_search(blocks, grid_size):
    return recursive_backtracking_search(Assignment(grid_size, blocks))


def recursive_backtracking_search(assignment):
    if assignment.is_complete_assignment:
        return assignment

    curr = assignment.next_star_to_assign
    for value in assignment.possible_values(curr):
        if assignment.is_valid(value):
            assignment.assign_value(curr, value)
            result = recursive_backtracking_search(assignment)
            if result:
                return result
            assignment.unassign_value(curr)
    print(assignment.total_states)
    return None


grid, grid_length = load_grid_file('grid8x8.txt')
stars = backtracking_search(grid, grid_length)
display_grid(grid, grid_length)
if stars:
    print(stars.star_values)
    display_grid(grid, grid_length, stars.star_values)
else:
    print('no solution found')
