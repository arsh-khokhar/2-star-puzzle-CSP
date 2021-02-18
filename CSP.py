import random


class Csp:
    """
    An csp of stars to spaces on a grid

    Attributes
        grid_size           Size of the grid (10x10 grid -> 10)
        blocks              2D array representing the blocks of the grid
        star_values         Current csp of grid positions to stars,
                            index 0,1 are for row 1, 2,3 for row 2,etc.
        complete_csp        True when every star has a value, False otherwise
        next_star_to_assign Next star to assign (without heuristic)
        min_domain_num      Of current unassigned stars, what is the smallest domain
        min_domain_size     Size of the min_domain_num domain
    """

    def __init__(self, grid_size: int, blocks: list):
        self.grid_size = grid_size
        self.blocks = blocks
        
        # dictionary to map each cell to a block
        # This would significantly reduce the block lookups later
        self.cell_block_map = {}
        for block_index, block in enumerate(blocks):
            for cell in block:
                self.cell_block_map[cell] = block_index

        self.star_values = []  # star 0,1 are in row 1, 2,3 in row 2 etc,
        
        for i in range(grid_size * 2):
            self.star_values.append(-1)

        self.star_domains = []
        # initialize domains for each star as its row
        for i in range(len(self.star_values)):
            self.star_domains.insert(i, list(
            range((int(i/2)) * self.grid_size + 1,
            (int(i/2) + 1) * self.grid_size + 1)))
        
        self.unassigned_stars = list(range(grid_size*2)) # indices of unassigned stars for forward-check. Initially all stars are unassigned

        self.block_occupancy = [0]*len(blocks)  # block occupancy, ranging from 0 to 2. If 2, then block is fully occupied
        self.column_occupancy = [0]*grid_size  # column occupancy, ranging from 0 to 2. If 2, the column is fully occupied

        self.complete_csp = False
        self.next_star_to_assign = 0

        self.min_domain_num = 0
        self.min_domain_size = grid_size

    def assign_value(self, star_num: int, value: int):
        """
        Set star_values[star_num] to value, update other variables

        :param star_num: Star to be assigned value
        :param value: value to assign
        """
        if self.star_values[star_num] == -1:
            self.column_occupancy[value % self.grid_size] += 1
            self.block_occupancy[self.cell_block_map[value]] += 1 
            self.star_values[star_num] = value
            self.next_star_to_assign = star_num + 1
            self.safe_remove(self.unassigned_stars, star_num)
        else:
            print('Attempting to assign a cell that is already assigned')

        if len(self.unassigned_stars) == 0:
            self.complete_csp = True

    def unassign_value(self, star_num: int):
        """
        Set star_values[star_num] to -1, update other variables

        :param star_num: Star to be assigned value
        """
        if self.star_values[star_num] != -1:
            value = self.star_values[star_num]
            self.block_occupancy[self.cell_block_map[value]] -= 1
            self.column_occupancy[value % self.grid_size] -= 1
            self.star_values[star_num] = -1
            self.next_star_to_assign = star_num
            self.unassigned_stars.append(star_num)
        else:
            print('Attempting to unassign a cell that is already unassigned')

    def propogate_constraints(self, star_num: int, value: int):
        """
        Propogate constraints based on the currently assigned star

        :param star_num: index of the star just assigned that will affect other stars' domains
        :return: False if domain wipeout (dead end) is detected, false otherwise
        """
        domain_size_dict = {}
        for star in self.unassigned_stars:
            if star == star_num:
                continue
            domain = self.star_domains[star]
            for cell in domain[:]:

                # since value is now occupied, it needs to get deleted from the domains of
                # remaining stars 
                if cell == value:
                    self.safe_remove(domain, cell)

                # remaining stars cannot be adjacent to value, so update domains accordingly
                if self.are_adjacent(cell, value):
                    self.safe_remove(domain, cell)

                # column occupancy constraint
                # check if the column is filled after putting value 
                # and update the remaining domains accordingly
                if self.column_occupancy[value % self.grid_size] >= 2 and \
                        self.same_col(cell, value):
                    self.safe_remove(domain, cell)

                # block occupancy constraint
                # cell_block_map[value] gives the index of block the value is in,
                # and the occupancy for the block at this index is checked
                if self.block_occupancy[self.cell_block_map[value]] >= 2 and \
                        self.same_block(cell, value):
                    self.safe_remove(domain, cell)

            domain_size_dict[star] = len(domain)

        if len(self.unassigned_stars) > 0:
            min_value = min(domain_size_dict.values())
            keys = [key for key, value in domain_size_dict.items() if value == min_value]
            chosen_min = random.choice(keys)

            self.min_domain_size = domain_size_dict[chosen_min]
            self.min_domain_num = chosen_min

    def same_row(self, star1: int, star2: int):
        """
        Check to see if two stars are in the same row

        :param star1: First star to be compared
        :param star2: Second star to be compared
        :return: True if the stars are in the same row, False otherwise
        """
        return int((star1 - 1) / self.grid_size) == int((star2 - 1) / self.grid_size)

    def same_col(self, star1: int, star2: int):
        """
        Check to see if two stars are in the same column

        :param star1: First star to be compared
        :param star2: Second star to be compared
        :return: True if the stars are in the same column, False otherwise
        """
        return star1 % self.grid_size == star2 % self.grid_size

    def same_block(self, star1: int, star2: int):
        """
        Check to see if two stars are in the same block

        :param star1: First star to be compared
        :param star2: Second star to be compared
        :return: True if the stars are in the same block, False otherwise
        """
        return self.cell_block_map[star1] == self.cell_block_map[star2]

    def are_adjacent(self, star1: int, star2: int):
        """
        Check to see if two stars are adjacent to each other.

        :param star1: First star to be compared
        :param star2: Second star to be compared
        :return: True if the stars are adjacent, False otherwise
        """
        # return statements can be removed heavily, but kept this
        #   for now for better readability
        if star1 == star2:  # same cell
            return True
        if star1 == star2 - self.grid_size:  # star2 on top
            return True
        if star1 == star2 + self.grid_size:  # star2 on bottom
            return True

        # check that star1 is not on right edge
        if star1 % self.grid_size != 0:
            # can safely detect the right neighbors here
            if star1 == star2 - 1:  # star2 on right
                return True
            if star1 == star2 - self.grid_size - 1:  # star2 on top-right
                return True
            if star1 == star2 + self.grid_size - 1:  # star2 on bottom-right
                return True

        # check that star1 is not on left edge
        if star1 % self.grid_size != 1:
            # can safely detect the left neighbors here
            if star1 == star2 + 1:  # star2 on left
                return True
            if star1 == star2 - self.grid_size + 1:  # star2 on top-left
                return True
            if star1 == star2 + self.grid_size + 1:  # star2 on bottom-left
                return True

        return False

    def is_valid(self, grid_index: int):
        """
        Check to see if grid_index being the next star location will be valid.
        Note that we only check constraints that would change because of
        the insertion, not the entire csp.

        :param grid_index: The grid location of the next star.
        :return: True if valid and False if invalid.
        """
        num_in_row = 0
        num_in_col = 0
        num_in_block = 0

        for star in self.star_values:
            if star != -1:
                if self.same_row(star, grid_index):
                    num_in_row += 1
                if self.same_col(star, grid_index):
                    num_in_col += 1
                if self.same_block(star, grid_index):
                    num_in_block += 1
                if self.are_adjacent(star, grid_index):
                    return False
                if num_in_row >= 2 \
                        or num_in_col >= 2 \
                        or num_in_block >= 2:
                    return False
        return True

    def heuristic_two(self):
        domain_size_diff_dict = {}

        original_domain_sizes_sum = self.sum_of_domain_sizes()
        domain_min_size_copy = self.min_domain_size
        domain_min_num_copy = self.min_domain_num
        for star in self.unassigned_stars:
            domain = self.star_domains[star]
            curr_domain_sizes_reduction = 0
            for cell in domain:
                domains_copy = [x[:] for x in self.star_domains]
                self.propogate_constraints(star, cell)
                curr_domain_sizes_reduction += original_domain_sizes_sum \
                                               - self.sum_of_domain_sizes()
                self.star_domains = [x[:] for x in domains_copy]
            domain_size_diff_dict[star] = curr_domain_sizes_reduction

        self.min_domain_size = domain_min_size_copy
        self.min_domain_num = domain_min_num_copy

        if len(self.unassigned_stars) > 0:
            max_value = max(domain_size_diff_dict.values())
            keys = [key for key, value in domain_size_diff_dict.items() if value == max_value]
            chosen_max = random.choice(keys)

            return chosen_max

    def sum_of_domain_sizes(self):
        domain_sizes_sum = 0
        for star in self.unassigned_stars:
            domain_sizes_sum += len(self.star_domains[star])
        return domain_sizes_sum

    def safe_remove(self, input_list: list, to_remove: int):
        """
        Attempt removing an element from a list without throwing any exceptions
        if the element was not found

        :param input_list: list from which the element has to be removed
        :param to_remove: element to be removed
        """
        try:
            input_list.remove(to_remove)
        except ValueError:
            # if we try to remove an element not in the list, don't do anything
            pass
