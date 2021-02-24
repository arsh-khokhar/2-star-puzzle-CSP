"""
    File name: CSP.py
    Author: Arsh Khokhar, Kiernan Weise
    Date last modified: 22 February, 2021
    Python Version: 3.8

    This script contains the CSP class for constructing a CSP instance
    of the 2-star constraint satisfaction problem
"""
import numpy as np
import time


class Csp:
    """
    A csp representation of the 2 star puzzle

    Attributes
        grid_size           Size of the grid (10x10 grid -> 10)
        blocks              2D array representing the blocks of the grid
        cell_map            A key value pair that maps each cell to its
                            block and the indices of the variables
        start_time          start time of the csp to keep track of its initialization
        ordering_choice     ordering choice based on the heuristic
        unassigned_vars     the list of variables that are currently unassigned
        domains             list of domains of all the variables
        block_occupancy     a list that keeps track of occupancy of each block, indexed
                                from 0 to number of blocks - 1
        row_occupancy       a list that keeps track of occupancy of each row, indexed from
                                0 to number of rows - 1
        col_occupancy       a list that keeps track of occupancy of each column, indexed 
                                from 0 to number of rows - 1
        num_edge_list       a list that keeps track of the number of edges incident to each
                                variable. indexing is done parallel to the index of variables
        last_num_edge_list  a list that runs one iteration behind of num_edge_list for restoring
                                vales when required
    """
    def __init__(self, blocks: list, grid_size: int, ordering_choice: int):
        """
        Constructor for a csp instance

        :param blocks: list of all the blocks in the grid
        :param grid_size: size of the input grid 
        :param ordering_choice: chosen heuristic for variable ordering (0,1,2 or 3)
        """
        num_stars = 2*grid_size  # for the 2 star problem
        self.grid_size = grid_size
        self.blocks = blocks
        self.cell_map = {}
        self.start_time = time.time()

        self.ordering_choice = ordering_choice  # chosen heuristic

        for i, block in enumerate(blocks):
            for cell in block:
                self.cell_map[cell] \
                    = {'block': i, 'in_domains_of': [2*i, 2*i + 1]}

        self.unassigned_vars = []
        for i in range(num_stars):
            self.unassigned_vars.append(i)

        self.domains = {}
        num_domains = 0
        for block in blocks:
            self.domains[num_domains] = set(block[:])   # deep copy required here
            self.domains[num_domains + 1] = set(block[:])
            num_domains += 2

        self.block_occupancy = [0]*len(blocks)
        self.row_occupancy = [0]*grid_size
        self.col_occupancy = [0]*grid_size

        self.num_edge_list = [num_stars]*num_stars

        self.last_num_edge_list = [num_stars]*num_stars

    def same_row(self, value1: int, value2: int):
        """
        Check if two values are in the same row of the grid

        :param value1: First value to be compared
        :param value2: Second value to be compared
        :return: True if the values are in the same row, False otherwise
        """
        return (value1 - 1) // self.grid_size == (value2 - 1) // self.grid_size

    def same_col(self, value1: int, value2: int):
        """
        Check if two values are in the same column of the grid

        :param value1: First value to be compared
        :param value2: Second value to be compared
        :return: True if the values are in the same column, False otherwise
        """
        return (value1 - 1) % self.grid_size == (value2 - 1) % self.grid_size

    def same_block(self, value1: int, value2: int):
        """
        Check if two values are in the same block

        :param value1: First value to be compared
        :param value2: Second value to be compared
        :return: True if the values are in the same block, False otherwise
        """
        return self.cell_map[value1]['block'] == self.cell_map[value2]['block']

    def is_col_occupied(self, value: int):
        """
        Check if the column in which a value belongs to is fully occupied 

        :param value: Value whose column occupancy is to be checked
        :return: True if the column is fully occupied, False otherwise
        """
        return self.col_occupancy[(value - 1) % self.grid_size] >= 2

    def is_row_occupied(self, value: int):
        """
        Check if the row in which a value belongs to is fully occupied 

        :param value: Value whose row occupancy is to be checked
        :return: True if the row is fully occupied, False otherwise
        """
        return self.row_occupancy[(value - 1)// self.grid_size] >= 2

    def is_block_occupied(self, value: int):
        """
        Check if the block in which a value belongs to is fully occupied 

        :param value: Value whose block occupancy is to be checked
        :return: True if the block is fully occupied, False otherwise
        """
        block = self.cell_map[value]['block']
        return self.block_occupancy[block] >= 2

    def are_adjacent(self, value1: int, value2: int):
        """
        Check if two values are adjacent to each other

        :param value1: First value to be compared
        :param value2: Second value to be compared
        :return: True if the values are adjacent, False otherwise
        """
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

    def is_consistent(self, value: int, assignment: dict):
        """
        Check if a value is consistent with an existing assignment

        :param value: Value whose consistency is to be checked
        :param assignment: existing assignment for consistency check
        :return: True if the value is consistent with the assignment, 
                 False otherwise
        """
        if self.is_col_occupied(value) or self.is_row_occupied(value) \
                or self.is_block_occupied(value):
            return False

        for val in assignment.values():
            if self.are_adjacent(value, val):
                return False

        return True

    def is_complete(self, assignment: dict):
        """
        Check if an assignment is complete for the 2-star csp

        :param assignment: Assignment to be checked
        :return: True if the assignment is complete, False otherwise
        """
        return len(assignment) == 2*self.grid_size

    def get_next_unassigned_var(self):
        """
        Get the next unassigned variable of csp based on the initial chosen heuristic

        :return: Next unassigned variable of the csp
        """
        # No heuristic
        if self.ordering_choice == 0:   
            return self.unassigned_vars[0]
        
        # Heuristic 1
        if self.ordering_choice == 1:
            return self.get_most_constrained()
        
        # Heuristic 2
        if self.ordering_choice == 2:
            return self.get_most_constraining()
        
        # Hybrid of Heuristic 1 and Heuristic 2
        if self.ordering_choice == 3:
            return np.random.choice([self.get_most_constraining(),
                                    self.get_most_constrained()], p=[0.1, 0.9])

    def get_most_constrained(self):
        """
        Get the most constrained unassigned variable of the csp
        by choosing the variable that has the smallest domain

        :return: the most constrained unassigned variable
        """
        most_constrained = self.unassigned_vars[0]  # default choice
        smallest_domain = self.domains[most_constrained]
        for var in self.unassigned_vars:
            if len(smallest_domain) > len(self.domains[var]):
                # smaller domain found, update accordingly
                smallest_domain = self.domains[var]
                most_constrained = var
        return most_constrained

    def get_most_constraining(self):
        index_max_edges = 0
        max_edges = 0
        for i, var in enumerate(self.unassigned_vars):
            if self.num_edge_list[var] > max_edges:
                max_edges = self.num_edge_list[var]
                index_max_edges = i
        return self.unassigned_vars[index_max_edges]

    def assign_val(self, var: int, value: int, assignment: dict):
        """
        Assign a value to a variable and update the related bookkeeping
        accordingly

        :param var: variable to which the value is to be assigned
        :param value: value to assign
        :param assignment: assignment in which the new value is to be added
        """
        assignment[var] = value
        row = (value - 1) // self.grid_size
        col = (value - 1) % self.grid_size
        self.row_occupancy[row] += 1
        self.col_occupancy[col] += 1
        block = self.cell_map[value]['block']  # the variable's block
        if self.ordering_choice == 2 or self.ordering_choice == 3:
            # if heuristic 2 or hybrid is chosen, edge incident is required
            # not done for heuristic 1 for performance gain
            self.last_num_edge_list = self.num_edge_list[:]
            self.incident_edges(value, row, col, assignment)
        self.block_occupancy[block] += 1
        self.safe_remove_list(self.unassigned_vars, var)

    def unassign_val(self, var: int, value: int, assignment: dict):
        """
        Unassign a variable and update the related bookkeeping
        accordingly

        :param var: variable to be unassigned
        :param value: value that is being unassigned
        :param assignment: assignment from which variable is to be removed
        """
        self.safe_remove_dict(assignment, var)  # safe removal to prevent failure
        row = (value - 1) // self.grid_size
        col = (value - 1) % self.grid_size
        self.row_occupancy[row] -= 1
        self.col_occupancy[col] -= 1
        block = self.cell_map[value]['block']  # the variable's block
        self.block_occupancy[block] -= 1 
        if self.ordering_choice == 2 or self.ordering_choice == 3:
            self.num_edge_list = self.last_num_edge_list[:]
        self.unassigned_vars.append(var)

    def update_edge(self, cell: int, assignment: dict):
        """
        Update the number of edges incident on a cell

        :param cell: cell associated with the block for which variables'
                    number of edges is to be updated
        :param assignment: assignment causing the update
        """
        if cell not in self.cell_map:
            return
        incident_block = self.cell_map[cell]['block']
        if 2*incident_block not in assignment:
            self.num_edge_list[2*incident_block] -= 1
        elif 2*incident_block + 1 not in assignment:
            self.num_edge_list[2*incident_block + 1] -= 1

    def incident_edges(self, value: int, row: int, col: int, assignment: dict):
        """
        Update the number of edges of the graph based on the assigned value

        :param value: value that was assigned
        :param row: row of the assigned value
        :param col: column of the assigned value
        :param assignment: set of already assigned variables
        """
        self.update_edge(value, assignment)  # updating the edge for the pairing star in the same block

        # updating the number of edges of all the cells in the same row
        for i in range(row*self.grid_size+1, row*self.grid_size+self.grid_size+1): 
            self.update_edge(i, assignment)
        
        # updating the number of edges of all the cells in the same column
        for i in range(col + 1, self.grid_size*(self.grid_size-1) + col + 1, self.grid_size):
            self.update_edge(i, assignment)
        
        # updating the number of edges of the adjacent cells
        if value % self.grid_size != 0:
            # can safely detect the left neighbors here
            # -1 is left, - self.grid_size - 1 is top-left, self.grid_size - 1 is bottom-left   
            for i in -1, -self.grid_size - 1, self.grid_size - 1:
                self.update_edge(value + i, assignment)

        if value % self.grid_size != 1:
            # can safely detect the right neighbors here
            # 1 is right, - self.grid_size + 1 is top-right, self.grid_size + 1 is bottom-right
            for i in 1, -self.grid_size + 1, self.grid_size+1:
                self.update_edge(value + i, assignment)
    
    def propagate_constraints(self, value: int, changed_domains: dict):
        """
        Reduce the domains of the remaining unassigned variables based on
        a value being assigned

        :param value: value being assigned
        :param changed_domains: temporary storage for storing a domain
                                before any changes. This will help in 
                                restoring values in case the assignment 
                                is failure
        :return: True if the propagation was successful, False if there
                was a domain wipeout detected
        """
        is_row_occupied = self.is_row_occupied(value)
        is_col_occupied = self.is_col_occupied(value)
        is_block_occupied = self.is_block_occupied(value)
        for var in self.unassigned_vars:
            domain = self.domains[var]
            domain_copy = list(domain)  # required for iterating over
            is_changed = False
            for cell in domain_copy:    # iterating over a copy so actual updates can happen
                if (self.same_row(cell, value) and is_row_occupied) or \
                    (self.same_col(cell, value) and is_col_occupied) or \
                    (self.same_block(cell, value) and is_block_occupied) or \
                        self.are_adjacent(value, cell):
                    is_changed = True   # mark that a domain was changed because of some removal
                    self.safe_remove_set(domain, cell)
                if len(domain) == 0:
                    # domain wipeout detected
                    if is_changed:  # still need to store the last good value for restoring later
                        changed_domains[var] = domain_copy
                    return False
            # if the current domain was changed because of some removal, keep the last copy in case
            # restoration is required later
            if is_changed:
                changed_domains[var] = domain_copy
        return True

    def restore_domains(self, changed_domains: dict):
        """
        Restores all the domains that were changed to their previous values

        :param changed_domains: dictionary of the previous (good) domains
        """
        for key in changed_domains:
            self.domains[key] = set(changed_domains[key])

    @staticmethod
    def safe_remove_list(input_list: list, value):
        """
        Deletes an entry from a list without throwing the ValueError exception
        in case the entry is not in the set

        :param input_list: set from which the entry has to be removed
        :param value: the set entry to be removed
        """
        try:
            input_list.remove(value)
        except ValueError:
            print("trying to remove something funky from a list")
            pass

    @staticmethod
    def safe_remove_set(input_set: set, value):
        """
        Deletes an entry from a set without throwing the KeyError exception
        in case the entry is not in the set

        :param input_set: set from which the entry has to be removed
        :param value: the set entry to be removed
        """
        try:
            input_set.remove(value)
        except KeyError:
            print("trying to remove something funky from a set")
            pass

    @staticmethod
    def safe_remove_dict(input_dict: dict, value):
        """
        Deletes an entry from a dictionary without throwing the KeyError exception
        in case the entry is not in the dictionary

        :param input_dict: dictionary from which the entry has to be removed
        :param value: the dictionary entry to be removed
        """
        try:
            del input_dict[value]
        except KeyError:
            print("trying to remove something funky from a dictionary")
            pass
