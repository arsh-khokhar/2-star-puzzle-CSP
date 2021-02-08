
class Assignment:
    def __init__(self, grid_size):
        self.values = []  # 2D array of stars on rows
        for i in range(grid_size):
            self.values.append([None] * 2)
        self.num_assigned = 0
        self.is_complete = False
        self.next_row_to_assign = 0

    def assign_value(self, row, value):
        if self.values[row][0] and not self.values[row][1]:
            self.values[row][1] = value
            self.next_row_to_assign = row+1
            self.num_assigned += 1
        elif not self.values[row][0]:
            self.values[row][0] = value
            # self.next_row_to_assign = row
            self.num_assigned += 1
        else:
            print('Attempting to assign a row that is already fully assigned')

        if self.num_assigned == 2 * len(self.values):
            self.is_complete = True

    def unassign_value(self, row):
        # note that stars in a row are always assigned l2r
        if self.values[row][1]:
            self.values[row][1] = None
            # self.next_row_to_assign = row
            self.num_assigned -= 1
        elif self.values[row][0]:
            self.values[row][0] = None
            self.next_row_to_assign = row - 1
            self.num_assigned -= 1
        else:
            print('Attempting to unassign a row that is already fully '
                  'unassigned')


def backtracking_search(grid, grid_size):
    return recursive_backtracking_search(Assignment(grid_size), grid)


def recursive_backtracking_search(assignment, grid):
    if assignment.is_complete:
        return assignment

    curr = assignment.next_row_to_assign
    for value in possible_values(assignment, curr):
        if is_valid(assignment, curr, value, grid):
            assignment[curr] = value
            result = recursive_backtracking_search(assignment, grid)
            if result:
                return result
            assignment.unassign_value(curr)
    return None


def possible_values(assignment, row):
    # any where in a specific row/column/block (we choose one and stick to it)
    return []


def is_valid(assignment, var, value, grid):
    # return true if setting var to value is a valid assignment

    # no two stars can be adjacent in any direction (king in chess)
    # no more than 2 elements per column/row/block
    return True
