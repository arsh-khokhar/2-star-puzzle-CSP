class Assignment:

    def __init__(self, grid_size, blocks):
        self.grid_size = grid_size
        self.blocks = blocks
        self.total_states = 0
        self.star_values = []  # star 0,1 are in row 1, 2,3 in row 2 etc,
        for i in range(grid_size * 2):
            self.star_values.append(-1)
        self.num_stars_assigned = 0
        self.is_complete_assignment = False
        self.next_star_to_assign = 0

    def assign_value(self, row, value):
        if self.star_values[row] == -1:
            self.star_values[row] = value
            self.next_star_to_assign = row + 1
            self.num_stars_assigned += 1
        else:
            print('Attempting to assign a row that is already fully assigned')

        if self.num_stars_assigned == 2 * self.grid_size:
            self.is_complete_assignment = True

    def unassign_value(self, row):
        # note that stars in a row are always assigned l2r
        if self.star_values[row] != -1:
            self.star_values[row] = -1
            self.next_star_to_assign = row
            self.num_stars_assigned -= 1
        else:
            print('Attempting to unassign a row that is already fully '
                  'unassigned')

    def possible_values(self, star_num: int):
        # if we're assigning the first star to a row, the star can go
        # anywhere in the row
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
        return int((star1-1)/self.grid_size) == int((star2-1)/self.grid_size)

    def same_col(self, star1: int, star2: int):
        return star1 % self.grid_size == star2 % self.grid_size

    def same_block(self, star1: int, star2: int):
        for block in self.blocks:
            if star1 in block and star2 in block:
                return True
            # a star can only be in one block, so if we find the block of one
            # star but not the other, they must be in different blocks
            elif star1 in block or star2 in block:
                return False
        return False

    def are_adjacent(self, star1: int, star2: int):
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

    def are_adjacent_helper(self, star1, star2):
        # star2 is in the same column as star1
        if star1 % self.grid_size == star2 % self.grid_size:
            return True
        # star2 is to the right of star1
        elif star1 % self.grid_size == (star2 % self.grid_size) - 1:
            return True
        # star2 is to the left of star1
        elif star1 % self.grid_size == (star2 % self.grid_size) + 1:
            return True

    def is_valid(self, grid_index: int):
        self.total_states += 1
        # might be useful to have hashed star values, but we'll worry about that later
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
