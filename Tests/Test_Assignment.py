from Assignment import Assignment
from main import load_grid_file


def init_assignment():
    blocks, grid_length = load_grid_file('grid8x8.txt')
    return Assignment(grid_length, blocks)


TEST_VALUES_TO_ASSIGN = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16]


def test_assign_value():
    assignment = init_assignment()
    for val in TEST_VALUES_TO_ASSIGN:
        assignment.assign_value(assignment.next_star_to_assign, val)
        assert assignment.star_values[val - 1] == val

    assert assignment.is_complete_assignment


def test_unassign_value():
    assignment = init_assignment()
    for val in TEST_VALUES_TO_ASSIGN:
        assignment.assign_value(assignment.next_star_to_assign, val)

    for i in range(len(TEST_VALUES_TO_ASSIGN) - 1, -1, -1):
        assert assignment.star_values[i] != -1
        assignment.unassign_value(i)
        assert assignment.star_values[i] == -1


TEST_POSSIBLE_VALUES = [(0, [1, 2, 3, 4, 5, 6, 7, 8]),
                        (1, [1, 2, 3, 4, 5, 6, 7, 8]),
                        (2, [9, 10, 11, 12, 13, 14, 15, 16]),
                        ]

TEST_ASSIGN_THEN_POSSIBLE_VALUES = [(6, 1, [1, 2, 3, 4, 8])]


def test_possible_values():
    assignment = init_assignment()
    for star_num, expected_list in TEST_POSSIBLE_VALUES:
        if not bool(set(assignment.possible_values(star_num))
                            .intersection(expected_list)):
            raise Exception("The case {0},{1} evaluated to {2}"
                            .format(star_num, expected_list,
                                    assignment.possible_values(star_num)))

    for value_to_assign, star_num, expected_list in \
            TEST_ASSIGN_THEN_POSSIBLE_VALUES:
        assignment.star_values[0] = value_to_assign
        if not bool(set(assignment.possible_values(star_num))
                            .intersection(expected_list)):
            raise Exception("The case {0},{1} evaluated to {2}"
                            .format(star_num, expected_list,
                                    assignment.possible_values(star_num)))
        assignment.star_values[0] = -1


TEST_SAME_ROW = [(1, 2, True), (1, 3, True), (1, 4, True), (1, 5, True),
                 (1, 6, True), (1, 7, True), (1, 8, True),
                 (9, 2, False), (9, 3, False), (9, 4, False), (9, 5, False),
                 (9, 6, False), (9, 7, False), (9, 8, False), ]


def test_same_row():
    assignment = init_assignment()
    for star1, star2, result in TEST_SAME_ROW:
        if assignment.same_row(star1, star2) != result:
            raise Exception("The case {0},{1},{2} didn't evaluate as expected"
                            .format(star1, star2, result))


TEST_SAME_COL = [(1, 9, True), (1, 17, True), (1, 25, True), (1, 33, True),
                 (1, 41, True), (1, 49, True), (1, 57, True),
                 (2, 10, True), (2, 18, True), (2, 26, True), (2, 34, True),
                 (2, 42, True), (2, 50, True), (2, 58, True),
                 (8, 9, False), (8, 17, False), (8, 25, False), (8, 33, False),
                 (8, 41, False), (8, 49, False), (8, 57, False), ]


def test_same_col():
    assignment = init_assignment()
    for star1, star2, result in TEST_SAME_COL:
        if assignment.same_col(star1, star2) != result:
            raise Exception("The case {0},{1},{2} didn't evaluate as expected"
                            .format(star1, star2, result))


TEST_SAME_BLOCK = [(1, 2, True), (1, 3, True), (1, 4, True), (1, 5, True),
                   (1, 6, True), (1, 6, True), (1, 7, True), (1, 8, True),
                   (1, 14, True), (1, 15, True), (1, 16, True), (1, 9, False),
                   (1, 10, False), (1, 11, False), (1, 20, False),
                   (1, 24, False), (1, 64, False), (1, 55, False), ]


def test_same_block():
    assignment = init_assignment()
    for star1, star2, result in TEST_SAME_BLOCK:
        if assignment.same_block(star1, star2) != result:
            raise Exception("The case {0},{1},{2} didn't evaluate as expected"
                            .format(star1, star2, result))


TEST_ARE_ADJACENT = [(10, 1, True), (10, 2, True), (10, 3, True),
                     (10, 9, True), (10, 11, True), (10, 17, True),
                     (10, 18, True), (10, 19, True),
                     (9, 8, False), (9, 16, False), (9, 24, False),
                     (16, 1, False), (16, 9, False), (16, 17, False),
                     (18, 1, False), (18, 2, False), (18, 3, False),
                     (18, 33, False), (18, 34, False), (18,35, False),]


def test_are_adjacent():
    assignment = init_assignment()
    for star1, star2, result in TEST_ARE_ADJACENT:
        if assignment.are_adjacent(star1, star2) != result:
            raise Exception("The case {0},{1},{2} didn't evaluate as expected"
                            .format(star1, star2, result))


TEST_IS_VALID = [(1, True), (2, False), (3, True), (5, False), (9, False),
                 (12, False), (13, True), (15, False), (17, True), (33, False)]


def test_is_valid():
    assignment = init_assignment()
    for grid_index, result in TEST_IS_VALID:
        if assignment.is_valid(grid_index) != result:
            raise Exception("The case {0},{1} didn't evaluate as expected"
                            .format(grid_index, result))
        elif result:
            assignment.assign_value(assignment.next_star_to_assign, grid_index)