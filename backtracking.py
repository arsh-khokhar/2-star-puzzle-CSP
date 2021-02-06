
def backtracking_search(grid):
    return recursive_backtracking_search({}, grid)


def recursive_backtracking_search(assignment, grid):
    if assignment['is complete']:  # probably a function or similar
        return assignment  # (the star locations)

    # select some var to assign, likely a list index
    curr = None  # this is where we'd use a heuristic
    for value in possible_values():
        if is_valid(assignment, curr, value):
            assignment[curr] = value
            result = recursive_backtracking_search(assignment, grid)
            if result:
                return result
            assignment[curr] = None
    return None


def possible_values():
    # any where in a specific row/column/block (we choose one and stick to it)
    return []


def is_valid(assignment, var, value):
    # return true if setting var to value is a valid assignment

    # no two stars can be adjacent in any direction (king in chess)
    # no more than 2 elements per column/row/block
    return True
