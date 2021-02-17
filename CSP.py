class Csp:
    """
    An csp of stars to spaces on a grid

    Attributes
        grid_size           Size of the grid (10x10 grid -> 10)
        blocks              2D array representing the blocks of the grid
        star_values         Current csp of grid positions to stars,
                            index 0,1 are for row 1, 2,3 for row 2,etc.
        num_stars_assigned  Number of stars assigned
        complete_csp True when every star has a value, False otherwise
        next_star_to_assign Next star to assign (without heuristic)
    """

    def __init__(self, grid_size: int, blocks: list):
        self.grid_size = grid_size
        self.blocks = blocks
        self.cells = {}
        for i, block in enumerate(blocks):
            for cell in block:
                self.cells[cell] = i

        self.star_values = []  # star 0,1 are in row 1, 2,3 in row 2 etc,
        
        for i in range(grid_size * 2):
            self.star_values.append(-1)

        self.star_domains = []
        for i in range(len(self.star_values)):
            self.star_domains.insert(i, self.calculate_row_indices(i))
        
        self.unassigned_stars = list(range(grid_size*2)) # indices of unassigned stars for forward-check. Initially all stars are unassigned

        self.block_occupancy = [0]*len(blocks)  # block occupancy, ranging from 0 to 2. If 2, then block is fully occupied
        self.column_occupancy = [0]*grid_size  # column occupancy, ranging from 0 to 2. If 2, the column is fully occupied
        
        self.num_stars_assigned = 0
        self.domain_wipeout = False
        self.complete_csp = False
        self.next_star_to_assign = 0

    def assign_value(self, star_num: int, value: int):
        """
        Set star_values[star_num] to value, update other variables

        :param star_num: Star to be assigned value
        :param value: Value to assign
        """
        if self.star_values[star_num] == -1:
            self.column_occupancy[value % self.grid_size] += 1
            self.block_occupancy[self.cells[value]] += 1 
            self.star_values[star_num] = value
            self.next_star_to_assign = star_num + 1
            self.num_stars_assigned += 1
            self.unassigned_stars.remove(star_num)
        else:
            print('Attempting to assign a cell that is already assigned')

        if self.num_stars_assigned == 2 * self.grid_size:
            self.complete_csp = True

    def calculate_row_indices(self, star_num: int):
        return list(
            range((int(star_num/2)) * self.grid_size + 1,
            (int(star_num/2) + 1) * self.grid_size + 1))
    
    def calculate_col_indices(self, star_value: int):
        return list(
            range(star_value % self.grid_size, 
            self.grid_size*(self.grid_size - 1) + star_value % self.grid_size + 1, 
            self.grid_size))

    def unassign_value(self, star_num: int):
        """
        Set star_values[star_num] to -1, update other variables

        :param star_num: Star to be assigned value
        """
        if self.star_values[star_num] != -1:
            value = self.star_values[star_num]
            self.block_occupancy[self.cells[value]] -= 1
            self.column_occupancy[value % self.grid_size] -= 1
            self.star_values[star_num] = -1
            self.next_star_to_assign = star_num
            self.num_stars_assigned -= 1
            self.unassigned_stars.append(star_num)
        else:
            print('Attempting to unassign a cell that is already unassigned')
    
    def propogate_constraints(self, star_num: int):
        value = self.star_values[star_num]
        # First star in the row, so the domain of next star in the row can be reduced for adjacency if it is unassigned
        for star in self.unassigned_stars:
            domain = self.star_domains[star]            
            
            #  removing adjacent cells from domain, if any
            self.safe_remove(domain, value) # the cell itself
            self.safe_remove(domain, value - self.grid_size) # top cell
            self.safe_remove(domain, value + self.grid_size) # bottom cell

            if value % self.grid_size != 0:
                self.safe_remove(domain, value + 1) # right cell
                self.safe_remove(domain, value - self.grid_size + 1) # top-right cell
                self.safe_remove(domain, value + self.grid_size + 1) # bottom-right cell
            
            if value % self.grid_size != 1:
                self.safe_remove(domain, value - 1) # left cell
                self.safe_remove(domain, value - self.grid_size - 1) # top-left cell
                self.safe_remove(domain, value + self.grid_size - 1) # bottom-left cell

            # column occupancy constraint
            if self.column_occupancy[value % self.grid_size] >= 2:
                for cell in domain[:]:
                    if cell % self.grid_size == value % self.grid_size:
                        self.safe_remove(domain, cell)
            
            # block occupancy constraint
            if self.block_occupancy[self.cells[value]] >= 2:
                for cell in domain[:]:
                    if cell in self.blocks[self.cells[value]]:
                        self.safe_remove(domain, cell)

            # detect domain wipeout
            if len(domain) == 0: 
                return False

        return True
        
    def same_row(self, star1: int, star2: int):
        """
        Check to see if two stars are in the same row

        :param star1: First star to be compared
        :param star2: Second star to be compared
        :return: True if the stars are in the same row, False otherwise
        """
        return int((star1-1)/self.grid_size) == int((star2-1)/self.grid_size)

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
        for block in self.blocks:
            if star1 in block and star2 in block:
                return True
            # a star can only be in one block, so if we find the block of one
            # star but not the other, they must be in different blocks
            elif star1 in block or star2 in block:
                return False
        return False

    def are_adjacent(self, star1: int, star2: int):
        """
        Check to see if two stars are adjacent to each other.

        :param star1: First star to be compared
        :param star2: Second star to be compared
        :return: True if the stars are adjacent, False otherwise
        """
        # check for wrap around
        if not (star1 % self.grid_size == 0
                and star2 % self.grid_size == 1) \
                and not (star1 % self.grid_size == 1
                         and star2 % self.grid_size == 0):
            # star2 is above star1
            if int((star1-1)/self.grid_size) - 1 \
                    == int((star2-1)/self.grid_size):
                return self.are_adjacent_helper(star1, star2)
            # star2 is one the same row as star1
            if int((star1 - 1) / self.grid_size) \
                    == int((star2 - 1) / self.grid_size):
                return self.are_adjacent_helper(star1, star2)
            # star2 is below star1
            if int((star1 - 1) / self.grid_size) + 1 \
                    == int((star2 - 1) / self.grid_size):
                return self.are_adjacent_helper(star1, star2)
        return False

    def are_adjacent_helper(self, star1: int, star2: int):
        """
        Check to see if two stars are adjacent to each other.

        :param star1: First star to be compared
        :param star2: Second star to be compared
        :return: True if the stars columns are the same or near, False otherwise
        """
        # star2 is in the same column as star1
        if star1 % self.grid_size == star2 % self.grid_size:
            return True
        # star2 is to the right of star1
        elif star1 % self.grid_size == (star2 % self.grid_size) - 1:
            return True
        # star2 is to the left of star1
        elif star1 % self.grid_size == (star2 % self.grid_size) + 1:
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
