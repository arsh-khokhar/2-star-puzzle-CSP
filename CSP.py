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
        self.star_values = []  # star 0,1 are in row 1, 2,3 in row 2 etc,
        for i in range(grid_size * 2):
            self.star_values.append(-1)
        self.num_stars_assigned = 0
        self.complete_csp = False
        self.next_star_to_assign = 0

    def assign_value(self, star_num: int, value: int):
        """
        Set star_values[star_num] to value, update other variables

        :param star_num: Star to be assigned value
        :param value: Value to assign
        """
        if self.star_values[star_num] == -1:
            self.star_values[star_num] = value
            self.next_star_to_assign = star_num + 1
            self.num_stars_assigned += 1
        else:
            print('Attempting to assign a row that is already fully assigned')

        if self.num_stars_assigned == 2 * self.grid_size:
            self.complete_csp = True

    def unassign_value(self, star_num: int):
        """
        Set star_values[star_num] to -1, update other variables

        :param star_num: Star to be assigned value
        """
        if self.star_values[star_num] != -1:
            self.star_values[star_num] = -1
            self.next_star_to_assign = star_num
            self.num_stars_assigned -= 1
        else:
            print('Attempting to unassign a row that is already fully '
                  'unassigned')

    def possible_values(self, star_num: int):
        """
        Get possible values that star_values[star_num] can take, a star can
        take any value in it's own row, except for ones taken by the other
        star in it's own row and the spaces beside it.

        :param star_num: Star to get possible values for
        :return: Array of possible grid indexes for star_values[star_num]
        """
        the_possible_values = list(
            range((int(star_num/2)) * self.grid_size + 1,
            (int(star_num/2) + 1) * self.grid_size + 1))

        if star_num % 2 == 1:
            try:
                the_possible_values.remove(self.star_values[star_num - 1])
                the_possible_values.remove(self.star_values[star_num - 1] + 1)
                the_possible_values.remove(self.star_values[star_num - 1] - 1)
            except ValueError:
                # if we try to remove an element not in the list, don't do anything
                pass

        return the_possible_values

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
