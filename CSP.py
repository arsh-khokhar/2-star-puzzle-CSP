import functools
import random
import time


class Csp:
    def __init__(self, blocks, grid_size, ordering_choice):
        self.num_stars = 2*grid_size # for the 2 star problem
        self.grid_size = grid_size
        self.blocks = blocks
        self.cell_map = {}
        self.start_time = time.time()

        self.ordering_choice = ordering_choice

        for i, block in enumerate(blocks):
            for cell in block:
                self.cell_map[cell] \
                    = {'block': i, 'in_domains_of': [2*i, 2*i + 1]}

        self.unassigned_vars = []
        for i in range(self.num_stars):
            self.unassigned_vars.append(i)

        self.domains = {}
        num_domains = 0
        for block in blocks:
            self.domains[num_domains] = set(block[:])
            self.domains[num_domains + 1] = set(block[:])
            num_domains += 2

        self.block_occupancy = [0]*len(blocks)
        self.row_occupancy = [0]*grid_size
        self.col_occupancy = [0]*grid_size

        self.num_cells_block_constrains \
            = self.calculate_num_cells_block_constrains()

    def same_row(self, value1, value2):
        return (value1 - 1) // self.grid_size == (value2 - 1) // self.grid_size

    def same_col(self, value1, value2):
        return value1 % self.grid_size == value2 % self.grid_size

    def same_block(self, value1, value2):
        return self.cell_map[value1]['block'] == self.cell_map[value2]['block']

    def is_col_occupied(self, value):
        return self.col_occupancy[value % self.grid_size] >= 2

    def is_row_occupied(self, value):
        return self.row_occupancy[(value - 1)// self.grid_size] >= 2

    def is_block_occupied(self, value):
        block = self.cell_map[value]['block']
        return self.block_occupancy[block] >= 2

    def are_adjacent(self, value1: int, value2: int):
        if value1 == value2 or \
            value1 == value2 - self.grid_size or \
            value1 == value2 + self.grid_size:
            return True

        # check that value1 is not on right edge
        if value1 % self.grid_size != 0:
            # can safely detect the right neighbors here
            if value1 == value2 - 1 or \
                value1 == value2 - self.grid_size - 1 or \
                 value1 == value2 + self.grid_size - 1:
                return True

        # check that value1 is not on left edge
        if value1 % self.grid_size != 1:
            # can safely detect the left neighbors here
            if value1 == value2 + 1 or \
                value1 == value2 - self.grid_size + 1 or \
                value1 == value2 + self.grid_size + 1:
                return True

        return False

    def is_consistent(self, value, assignment):
        if self.is_col_occupied(value) or self.is_row_occupied(value) \
                or self.is_block_occupied(value):
            return False

        for val in assignment.values():
            if self.are_adjacent(value, val):
                return False

        return True

    def is_complete(self, assignment):
        return len(assignment) == 2*self.grid_size

    def get_next_unassigned_var(self):
        if self.ordering_choice == 0:
            return self.unassigned_vars[0]
        if self.ordering_choice == 1:
            return self.get_most_constrained()
        if self.ordering_choice == 2:
            return self.get_most_constraining()
        if self.ordering_choice == 3:
            return random.choice([self.get_most_constraining(),
                                  self.get_most_constrained()])

    def get_most_constrained(self):
        most_constrained = self.unassigned_vars[0]
        smallest_domain = self.domains[most_constrained]
        for var in self.unassigned_vars:
            if len(smallest_domain) > len(self.domains[var]):
                smallest_domain = self.domains[var]
                most_constrained = var
        return most_constrained

    def assign_val(self, var, value, assignment):
        assignment[var] = value
        self.row_occupancy[(value - 1) // self.grid_size] += 1
        self.col_occupancy[value % self.grid_size] += 1
        block = self.cell_map[value]['block']
        self.block_occupancy[block] += 1
        self.safe_remove_list(self.unassigned_vars, var)

    def unassign_val(self, var, value, assignment):
        self.safe_remove_dict(assignment, var)
        self.row_occupancy[(value - 1) // self.grid_size] -= 1
        self.col_occupancy[value % self.grid_size] -= 1
        block = self.cell_map[value]['block']
        self.block_occupancy[block] -= 1
        self.unassigned_vars.append(var)

    def propogate_constraints(self, value, removed_domains):
        is_row_occupied = self.is_row_occupied(value)
        is_col_occupied = self.is_col_occupied(value)
        is_block_occupied = self.is_block_occupied(value)
        for var in self.unassigned_vars:
            domain = self.domains[var]
            domain_copy = list(domain)
            is_removed = False
            for cell in domain_copy:
                if (self.same_row(cell, value) and is_row_occupied) or \
                    (self.same_col(cell, value) and is_col_occupied) or \
                    (self.same_block(cell, value) and is_block_occupied) or \
                        self.are_adjacent(value, cell):
                    is_removed = True
                    self.safe_remove_set(domain, cell)
                if len(domain) == 0:
                    # domain wipeout
                    if is_removed:
                        removed_domains[var] = domain_copy
                    return False
            if is_removed:
                removed_domains[var] = domain_copy
        return True

    def calculate_num_cells_block_constrains(self):
        num_cells_block_constrains = {}
        for block_num, block in enumerate(self.blocks):
            cells_affected = []
            for cell in block:
                for i in range(1, pow(self.grid_size, 2) + 1):
                    if cell not in cells_affected and i not in block \
                            and (self.same_row(cell, i)
                                 or self.same_col(cell, i)
                                 or self.same_block(cell, i)
                                 or self.are_adjacent(i, cell)):
                        cells_affected.append(i)
            num_cells_block_constrains[block_num] = len(cells_affected)
        return sorted(num_cells_block_constrains.items(),
                      key=functools.cmp_to_key(self.compare_with_ties))

    # TODO: So apparently I was sorting the wrong way (low-high vs high-low)
    #    and h2 is just as bad as before (80 000 000+ states) this kinda makes
    #    sense since we favour larger blocks, which have larger domains at higher
    #    levels, which isn't good (we move slower through domains at higher levels,
    #    hence the search takes longer).
    #  We could do an average cells affected per cell in a block to mitigate this,
    #    but I'm not sure that's correct.
    #  With that said, the code does work how planned it to.
    def get_most_constraining(self):
        # num_cells_block_constrains is already sorted by value, high to low
        for block_num, value \
                in self.num_cells_block_constrains:
            if block_num*2 in self.unassigned_vars:
                return block_num*2
            elif block_num*2 + 1 in self.unassigned_vars:
                return block_num*2 + 1

    def restore_domains(self, removed_domains):
        for key in removed_domains:
            self.domains[key] = set(removed_domains[key])

    @staticmethod
    def compare_with_ties(a, b):
        diff = b[1] - a[1]
        return diff if diff else random.choice([-1, 1])

    @staticmethod
    def safe_remove_list(input_list, value):
        try:
            input_list.remove(value)
        except ValueError:
            print("trying to remove something funky from a list")
            pass

    @staticmethod
    def safe_remove_set(input_set, value):
        try:
            input_set.remove(value)
        except KeyError:
            print("trying to remove something funky from a set")
            pass

    @staticmethod
    def safe_remove_dict(input_dict, value):
        try:
            del input_dict[value]
        except KeyError:
            print("trying to remove something funky from a dictionary")
            pass
